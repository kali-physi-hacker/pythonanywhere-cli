pythonanywhere-cli
==============

*A PythonAnywhere Command Line Interface.*

.. image:: https://travis-ci.org/cfc603/pythonanywhere-cli.png?branch=master
    :target: https://travis-ci.org/cfc603/pythonanywhere-cli

.. image:: https://codecov.io/github/cfc603/pythonanywhere-cli/coverage.svg?branch=master
    :target: https://codecov.io/github/cfc603/pythonanywhere-cli?branch=master

Usage
-----

Set you environment variables::

    # Your API_KEY can be found at https://www.pythonanywhere.com/account and select the "API token" tab.
    $ export PYTHONANYWHERE_CLI_API_KEY="API_KEY"

    # Your PythonAnywhere username
    $ export PYTHONANYWHERE_CLI_USER="USER"


Webapps::

    # Create a new webapp
    $ pythonanywhere webapps create username.pythonanywhere.com python27

    # Delete a webapp
    $ pythonanywhere webapps delete username.pythonanywhere.com

    # Reload Webapp
    $ pythonanywhere webapps reload username.pythonanywhere.com

    # Update Webapp python version or virtualenv path
    $ pythonanywhere webapps update username.pythonanywhere.com --python_version=2.7 --virtualenv_path=/path/to/env


Static File Mappings::

    # Create new static mapping
    $ pythonanywhere static_mapping create username.pythonanywhere.com /static/ /path/to/static

    # Delete static mapping
    $ pythonanywhere static_mapping delete username.pythonanywhere.com 123456

    # Display a list of static mappings
    $ pythonanywhere static_mapping list username.pythonanywhere.com

    # Update a static mapping url and/or path
    $ pythonanywhere static_mapping update username.pythonanywhere.com --url=/new-static/ --path=/new/path/to/static


Help::

    # Display help
    $ pythonanywhere -h


Credit
------

This application uses Open Source components. You can find the source code of their open source projects along with license information below. We acknowledge and are grateful to these developers for their contributions to open source.

:Project: helper_scripts https://github.com/pythonanywhere/helper_scripts
:Copyright: Copyright (c) 2017 PythonAnywhere LLP
:License: (MIT) https://github.com/pythonanywhere/helper_scripts/blob/master/LICENSE
