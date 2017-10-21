import os

from pythonanywhere_wrapper.client import PythonAnywhere, PythonAnywhereError

from .snakesay import snakesay


class Command(object):

    COMMANDS = []

    client = None

    def __init__(self, options, *args, **kwargs):
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.client = self.get_client()

    def get_client(self):
        api_key = self.options["--api_key"]
        user = self.options["--user"]

        if not api_key:
            api_key = os.environ["PYTHONANYWHERE_CLI_API_KEY"]

        if not user:
            user = os.environ["PYTHONANYWHERE_CLI_USER"]

        return PythonAnywhere(api_key=api_key, user=user)

    def run(self):
        for command in self.COMMANDS:
            if command in self.options and self.options[command]:
                command_function = getattr(self, command)
                try:
                    message = command_function()
                    print(snakesay(message))
                except PythonAnywhereError as error:
                    print(snakesay(error.args[0]))


class StaticFile(Command):

    COMMANDS = [
        "create",
        "delete",
        "list",
        "update",
    ]

    def create(self):
        domain_name = self.options["<domain_name>"]
        url = self.options["<url>"]
        path = self.options["<path>"]

        self.client.webapps.static_files.create(
            domain_name=domain_name, data={
                "url": url, "path": path
            }
        )

        return ("Static File mapping created for domain {} with url {} and"
                " path {}").format(domain_name, url, path)

    def delete(self):
        domain_name = self.options["<domain_name>"]
        static_id = self.options["<static_id>"]

        self.client.webapps.static_files.delete(
            domain_name=domain_name, static_id=static_id
        )

        return ("Static File mapping {} for domain {} has been"
                " removed.").format(static_id, domain_name)

    def list(self):
        domain_name = self.options["<domain_name>"]

        response = self.client.webapps.static_files(domain_name=domain_name)

        message = "Static File mappings for domain {}:".format(domain_name)
        counter = 0
        for mapping in response.json():
            counter += 1
            message += "  {}. ID: {} URL: {} Path: {}".format(
                counter,
                mapping["id"],
                mapping["url"],
                mapping["path"],
            )

        return message

    def update(self):
        domain_name = self.options["<domain_name>"]
        static_id = self.options["<static_id>"]
        url = self.options["--url"]
        path = self.options["--path"]

        if not url and not path:
            return ("You should supply a url or path to make any updates.")

        data = {}
        if url:
            data["url"] = url
        if path:
            data["path"] = path

        self.client.webapps.static_files.update(
            domain_name=domain_name, static_id=static_id, data=data
        )

        message = "Static File {} for domain {} was updated.".format(
            static_id, domain_name
        )
        if url:
            message += " URL: {}".format(url)
        if path:
            message += " Path: {}".format(path)

        return message


class Webapps(Command):

    COMMANDS = [
        "create",
        "delete",
        "reload",
        "update",
    ]

    def create(self):
        domain_name = self.options["<domain_name>"]
        python_version = self.options["<python_version>"]

        self.client.webapps.create(data={
                "domain_name": domain_name,
                "python_version": python_version,
        })

        return ("Webapp created with domain {}"
                " using python version {}.").format(
                domain_name, python_version
            )

    def delete(self):
        domain_name = self.options["<domain_name>"]

        self.client.webapps.delete(domain_name=domain_name)

        return ("Webapp with domain {} deleted.").format(domain_name)

    def reload(self):
        domain_name = self.options["<domain_name>"]

        self.client.webapps.reload(domain_name=domain_name)

        return ("Webapp with domain {} has been reloaded.").format(
            domain_name
        )

    def update(self):
        domain_name = self.options["<domain_name>"]
        virtualenv_path = self.options["--virtualenv_path"]
        python_version = self.options["--python_version"]

        if not virtualenv_path and not python_version:
            return ("You should supply a virtualenv_path or python_version to"
                    " make any updates.")

        data = {}
        if virtualenv_path:
            data["virtualenv_path"] = virtualenv_path
        if python_version:
            data["python_version"] = python_version

        self.client.webapps.update(
            domain_name=domain_name, data=data
        )

        message = "Webapp with domain {} was updated.".format(domain_name)
        if python_version:
            message += " Python Version: {}".format(python_version)
        if virtualenv_path:
            message += " Virtualenv Path: {}".format(virtualenv_path)

        return message
