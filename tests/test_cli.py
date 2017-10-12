from mock import patch

from pythonanywhere_cli.cli import main


@patch("pythonanywhere_cli.cli.Webapps")
@patch("pythonanywhere_cli.cli.docopt")
def test_main(docopt, Webapps):
    docopt.return_value = {"webapps": True}
    main()
    Webapps.assert_called_with({"webapps": True})
    Webapps.return_value.run.assert_called_once()
