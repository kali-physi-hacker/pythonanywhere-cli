from mock import patch

from pythonanywhere.client import PythonAnywhereError
from pythonanywhere_cli.commands import Command, StaticFile, Webapps


class TestCommand(object):

    class CommandException(Command):

        COMMANDS = [
            "exception"
        ]

        def exception(self):
            raise PythonAnywhereError("Test Exception")

    @patch("pythonanywhere_cli.commands.snakesay")
    def test_run_exception(self, snakesay):
        command_exception = self.CommandException({"exception": True})
        command_exception.run()
        snakesay.assert_called_with("Test Exception")


class TestStaticFile(object):

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_create(self, mock_client, snakesay):
        static_file = StaticFile({
                "create": True,
                "<domain_name>": "tests.domain.com",
                "<url>": "/url/",
                "<path>": "/path/"
            })
        static_file.run()
        client_call = static_file.client.webapps.static_files.create

        client_call.assert_called_with(
            data={'url': '/url/', 'path': '/path/'},
            domain_name='tests.domain.com'
        )
        snakesay.assert_called_with((
            "Static File mapping created for domain"
            " tests.domain.com with url /url/ and path /path/"
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_delete(self, mock_client, snakesay):
        static_file = StaticFile({
                "delete": True,
                "<domain_name>": "tests.domain.com",
                "<static_id>": "123"
            })
        static_file.run()
        client_call = static_file.client.webapps.static_files.delete

        client_call.assert_called_with(
            domain_name="tests.domain.com", static_id="123"
        )
        snakesay.assert_called_with((
            "Static File mapping 123 for domain"
            " tests.domain.com has been removed."
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_list(self, mock_client, snakesay):
        static_file = StaticFile({
                "list": True,
                "<domain_name>": "tests.domain.com",
            })
        client_call = static_file.client.webapps.static_files
        client_call.return_value.json.return_value = [
            {u'url': u'/static/', u'path': u'/static/', u'id': 123},
        ]
        static_file.run()

        client_call.assert_called_with(
            domain_name="tests.domain.com"
        )
        snakesay.assert_called_with((
            "Static File mappings for domain tests.domain.com:  1. ID: 123"
            " URL: /static/ Path: /static/"
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    def test_update_if_not_url_if_not_path(self, snakesay):
        static_file = StaticFile({
                "update": True,
                "<domain_name>": "tests.domain.com",
                "<static_id>": "123",
                "--url": None,
                "--path": None,
            })
        static_file.run()

        snakesay.assert_called_with((
            "You should supply a url or path to make"
            " any updates."
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_update_if_url(self, mock_client, snakesay):
        static_file = StaticFile({
                "update": True,
                "<domain_name>": "tests.domain.com",
                "<static_id>": "123",
                "--url": "/url/",
                "--path": None,
            })
        static_file.run()
        client_call = static_file.client.webapps.static_files.update

        client_call.assert_called_with(
            domain_name="tests.domain.com",
            static_id="123",
            data={"url": "/url/"}
        )
        snakesay.assert_called_with((
            "Static File 123 for domain"
            " tests.domain.com was updated. URL: /url/"
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_update_if_path(self, mock_client, snakesay):
        static_file = StaticFile({
                "update": True,
                "<domain_name>": "tests.domain.com",
                "<static_id>": "123",
                "--url": None,
                "--path": "/path/",
            })
        static_file.run()
        client_call = static_file.client.webapps.static_files.update

        client_call.assert_called_with(
            domain_name="tests.domain.com",
            static_id="123",
            data={"path": "/path/"}
        )
        snakesay.assert_called_with((
            "Static File 123 for domain"
            " tests.domain.com was updated. Path: /path/"
        ))


class TestWebapps(object):

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_create(self, mock_client, snakesay):
        webapp = Webapps({
                "create": True,
                "<domain_name>": "tests.domain.com",
                "<python_version>": "python27",
            })
        webapp.run()
        client_call = webapp.client.webapps.create

        client_call.assert_called_with(
            data={
                "domain_name": "tests.domain.com", "python_version": "python27"
            },
        )
        snakesay.assert_called_with((
            "Webapp created with domain"
            " tests.domain.com using python version python27."
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_delete(self, mock_client, snakesay):
        webapp = Webapps({
                "delete": True,
                "<domain_name>": "tests.domain.com",
            })
        webapp.run()
        client_call = webapp.client.webapps.delete

        client_call.assert_called_with(domain_name="tests.domain.com")
        snakesay.assert_called_with((
            "Webapp with domain"
            " tests.domain.com deleted."
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_reload(self, mock_client, snakesay):
        webapp = Webapps({
                "reload": True,
                "<domain_name>": "tests.domain.com",
            })
        webapp.run()
        client_call = webapp.client.webapps.reload

        client_call.assert_called_with(domain_name="tests.domain.com")
        snakesay.assert_called_with((
            "Webapp with domain"
            " tests.domain.com has been reloaded."
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    def test_update_if_not_virtualenv_path_if_not_python_vers(self, snakesay):
        webapp = Webapps({
                "update": True,
                "<domain_name>": "tests.domain.com",
                "--virtualenv_path": None,
                "--python_version": None,
            })
        webapp.run()

        snakesay.assert_called_with((
            "You should supply a virtualenv_path or"
            " python_version to make any updates."
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_update_if_virtualenv_path(self, mock_client, snakesay):
        webapp = Webapps({
                "update": True,
                "<domain_name>": "tests.domain.com",
                "--virtualenv_path": "/path/",
                "--python_version": None,
            })
        webapp.run()
        client_call = webapp.client.webapps.update

        client_call.assert_called_with(
            domain_name="tests.domain.com", data={"virtualenv_path": "/path/"}
        )
        snakesay.assert_called_with((
            "Webapp with domain tests.domain.com"
            " was updated. Virtualenv Path: /path/"
        ))

    @patch("pythonanywhere_cli.commands.snakesay")
    @patch("pythonanywhere_cli.commands.PythonAnywhere")
    def test_update_if_python_version(self, mock_client, snakesay):
        webapp = Webapps({
                "update": True,
                "<domain_name>": "tests.domain.com",
                "--virtualenv_path": None,
                "--python_version": "python27",
            })
        webapp.run()
        client_call = webapp.client.webapps.update

        client_call.assert_called_with(
            domain_name="tests.domain.com", data={"python_version": "python27"}
        )
        snakesay.assert_called_with((
            "Webapp with domain tests.domain.com"
            " was updated. Python Version: python27"
        ))
