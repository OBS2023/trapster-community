<p align="center">
    <br/>
    <a href="https://trapster.cloud">trapster.cloud</a>
    ·
    <a href="https://ballpoint.fr/">ballpoint.fr</a>
</p>
<div align="center">
<img src="./logo.png" height="200">
</div>


# Trapster Community

![License](https://img.shields.io/badge/license-AGPLv3+-blue)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Status](https://img.shields.io/badge/status-Production/Stable-green)

Trapster Community is a low-interaction honeypot designed to be deployed on internal networks. It is built to monitor and detect suspicious activities, providing a deceptive layer to network security.

Visit the [Trapster website](https://trapster.cloud) to learn more about our commercial product, which includes advanced features like pre-configured hardened OS, automatic deployment, webhook, and SIEM integration.

## Features

- **Deceptive Security**: Mimics network services to lure and detect potential intruders.
- **Asynchronous Framework**: Utilizes Python's `asyncio` for efficient, non-blocking operations.
- **Configuration Management**: Easily configurable through `trapster.conf`.
- **Expandable Services**: Add and configure as many services as needed with minimal effort.

## Installation

To install Trapster, clone the repository and use `setup.py` to install the dependencies:

```bash
git clone https://github.com/0xBallpoint/trapster.git
cd trapster
python -m venv venv
source ./venv/bin/activate
python setup.py install
```

## Usage
### Running the Daemon

After installation, to start the Trapster daemon, simply use the trapster command inside your folder:

```bash
trapster
```

## Configuration

Trapster uses a configuration file located at `data/trapster.conf`. Ensure the configuration file is correctly set up before running the daemon.
You can add as many services as you want.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add new feature').
5. Push to the branch (git push origin feature-branch).
6. Create a pull request.

## License

Trapster is licensed under the GNU Affero General Public License v3 or later (AGPLv3+). See the LICENSE file for more details.

