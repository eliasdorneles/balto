# ![Logo of Balto](logo-100x.png) BALTO
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors)

`BAlto is a Language independent Test Orchestrator` is an unique tool to drive
all your test-runners with one common interface.

## Installation

- Download the latest binary for you platform here: https://github.com/Lothiraldan/balto/releases
- Put the binary somewhere in your path
- Enjoy!

## Usage

To use it, point balto to a directory containing a `.balto.json` file:
    
```bash
balto tests/
```

The `.balto.json` file should look like:

```json
[{"tool": "pytest", "name": "Acceptance Test Suite Subprocess"}]

```

The tool must be one of the supported one, you can see the list here: https://github.com/lothiraldan/litf#compatible-emitters

You can test balto against examples for supported test runners. Clone this repository and launch `balto` against one of the examples directories. For `pytest`, launch:

```bash
balto examples/pytest/
```

For more help:

```bash
balto --help
```


## Development

Balto is composed of two components: the server and the web interface.

> Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its terms. Please report unacceptable behavior to [lothiraldan@gmail.com](lothiraldan@gmail.com).

### Balto-server

Balto-server is a Python 3.7 project using Asyncio. To build the development version, first create a virtualenv (or equivalent):

```bash
virtualenv .venv
source .venv/bin/activate
```

Install the project in development mode:

```bash
pip install -e .
```

Then start the server:

```bash
balto-server --debug examples/pytest/
```

The server will start on port 8889.

### Web interface

The web interface is a React project communicating with the server using WebSockets. You can start developing on it with these instructions:

```bash
cd balto/web_interfaces/balto_react
yarn start
```

The web interface is then available on http://localhost:3000/ and will connect to the server started before.

Warning: the WebSocket doesn't auto-reconnect yet, sometimes your React modification requires you to reload your browser tab.

## Contributors

Thanks goes to these wonderful people ([emoji key](https://github.com/kentcdodds/all-contributors#emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
| [<img src="https://avatars2.githubusercontent.com/u/243665?v=4" width="100px;"/><br /><sub><b> Boris Feld</b></sub>](https://lothiraldan.github.io/)<br />[💻](https://github.com/lothiraldan/balto/commits?author=Lothiraldan "Code") [🎨](#design-Lothiraldan "Design") [📖](https://github.com/lothiraldan/balto/commits?author=Lothiraldan "Documentation") [🤔](#ideas-Lothiraldan "Ideas, Planning, & Feedback") [📢](#talk-Lothiraldan "Talks") | [<img src="https://avatars0.githubusercontent.com/u/37565?v=4" width="100px;"/><br /><sub><b>Elias Dorneles</b></sub>](https://eliasdorneles.github.io)<br />[💻](https://github.com/lothiraldan/balto/commits?author=eliasdorneles "Code") [🐛](https://github.com/lothiraldan/balto/issues?q=author%3Aeliasdorneles "Bug reports") |
| :---: | :---: |
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification. Contributions of any kind welcome!