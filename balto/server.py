""" BAlto is a Language independent Test Orchestrator.
"""
from __future__ import print_function, unicode_literals

import argparse
import asyncio
import json
import logging
import sys
from os.path import dirname, isfile, join

import aiohttp
from aiohttp.web import Application, FileResponse, HTTPNotFound, run_app
from aiohttp_json_rpc import JsonRpc

from balto._logging import setup_logging
from balto.config import read_config
from balto.event_emitter import EventEmitter
from balto.store import Tests, SingleTest, MultipleTestSuite

LOGGER = logging.getLogger(__name__)


SUITES = MultipleTestSuite()


async def process_notification(message):
    msg_type = message.pop("_type")
    if msg_type == "test_collection":
        process_test_collection(message, SUITES)
    elif msg_type == "test_result":
        process_test_result(message, SUITES)
    else:
        print("Message", message)


def get_static_path():
    if getattr(sys, "frozen", False):
        return join(sys._MEIPASS, "balto/web_interfaces")
    else:
        return join(dirname(__file__), "web_interfaces")


def process_test_collection(message, suites):
    suite = message["suite_name"]
    # The run_id doesn't make sense here
    message.pop("run_id")
    suites[suite].update_test(message)


def process_test_result(message, suites):
    suite = message["suite_name"]
    suites[suite].update_test(message)


async def interface_handle(request):
    interface_name = request.match_info["interface"]
    local_directory = join(dirname(__file__), "web_interfaces", interface_name)
    index_file = join(local_directory, "index.html")

    if not isfile(index_file):
        index_file = join(local_directory, "build", "index.html")

    if isfile(index_file):
        return FileResponse(index_file)
    return HTTPNotFound()


def server(directory, runner):
    loop = asyncio.get_event_loop()

    # EM
    em = EventEmitter(loop)

    # Read config
    config_filepath = join(directory, ".balto.json")
    suites = read_config(config_filepath, runner, em)

    # Tests
    tests = Tests(suites)

    async def collect_all(request):
        LOGGER.info("Collect ALL")
        tasks = [
            suite.collect_all(directory, em, loop=loop) for suite in suites.values()
        ]
        await asyncio.gather(*tasks, loop=loop)
        return "ok"

    async def run_all(request):
        LOGGER.info("Run ALL")
        tasks = [
            suite.launch_all(directory, em, loop=loop) for suite in suites.values()
        ]
        await asyncio.gather(*tasks, loop=loop)
        return "ok"

    async def run_selected(request):
        tasks = []
        LOGGER.info("Run selected: %r", request.params)
        for suite_name, suite_tests in request.params.items():
            suite = suites[suite_name]
            tasks.append(suite.launch_tests(directory, em, loop, suite_tests))

        await asyncio.gather(*tasks)
        return "ok"

    rpc = JsonRpc()
    logging.getLogger("aiohttp-json-rpc.server").setLevel(logging.DEBUG)

    async def forward_notifications(message):
        LOGGER.debug("Forwarding to %d clients: %r", len(rpc.clients), message)
        for client in rpc.clients:
            data = {"jsonrpc": "2.0", "id": None, "method": "test", "params": message}
            r = await client.ws.send_str(json.dumps(data))

    em.register(forward_notifications)
    em.register(process_notification)

    loop = asyncio.get_event_loop()
    rpc.add_methods(("", collect_all), ("", run_selected), ("", run_all))
    rpc.add_topics("test")

    app = Application(loop=loop, debug=True)
    web_interfaces_route = get_static_path()
    app.router.add_static(
        "/interface/", web_interfaces_route, show_index=True, name="static"
    )
    app.router.add_route("*", "/", rpc)

    run_app(app, port=8889)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory", help="The directory LITR should start looking for its config file"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        help="activate the verbose mode",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--debug", help="activate the debug mode", action="store_true", default=False
    )
    parser.add_argument(
        "--runner",
        "-r",
        help="which runner to use",
        action="store",
        default="subprocess",
    )
    args = parser.parse_args()

    setup_logging(args.verbose, args.debug)

    server(args.directory, args.runner)


if __name__ == "__main__":
    main()
