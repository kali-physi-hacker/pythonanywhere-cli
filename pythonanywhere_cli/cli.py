""" # flake8: noqa
pythonanywhere

Usage:
    pythonanywhere webapps create <domain_name> <python_version> [--api_key=<api_key>] [--user=<user>]
    pythonanywhere webapps delete <domain_name> [--api_key=<api_key>] [--user=<user>]
    pythonanywhere webapps reload <domain_name> [--api_key=<api_key>] [--user=<user>]
    pythonanywhere webapps update <domain_name> [--python_version=<python_version>] [--virtualenv_path=<virtualenv_path>] [--api_key=<api_key>] [--user=<user>]
    pythonanywhere static_mapping create <domain_name> <url> <path> [--api_key=<api_key>] [--user=<user>]
    pythonanywhere static_mapping delete <domain_name> <static_id> [--api_key=<api_key>] [--user=<user>]
    pythonanywhere static_mapping list <domain_name> [--api_key=<api_key>] [--user=<user>]
    pythonanywhere static_mapping update <domain_name> <static_id> [--url=<url>] [--path=<path>] [--api_key=<api_key>] [--user=<user>]
    pythonanywhere -h | --help
    pythonanywhere --version

Options:
    -h --help                         Show this screen.
    --version                         Show version.

Help:
    For help using this tool, please open an issue on the Github repository:
    https://github.com/cfc603/pythonanywhere-cli
"""


from docopt import docopt

from . import __version__ as VERSION
from .commands import StaticFile, Webapps


COMMANDS = {
    "webapps": "Webapps",
    "static_mapping": "StaticFile",
}


def main():
    options = docopt(__doc__, version=VERSION)
    for command, command_class in COMMANDS.items():
        if command in options and options[command]:
            command_instance = globals()[command_class](options)
            command_instance.run()
