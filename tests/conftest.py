"""
Basic infrastructure for CEM tests using pytest
"""

import arrow
import collections
import datetime
import inspect
import logging
import os
import petl
import pytest
import re
import sqlalchemy.orm

from hextopia.config import HexConfig
from cem.utilities.app import create_app, db

@pytest.fixture(scope='session')
def find_data_file():
    """
    This fixture provides a function that finds a test data file based on the
    filename. It will look in the data subfolder of the calling function's
    directory

    .. code-block:: python
        :caption: example usage

        test_file_path = find_data_file('my_data.json')
    """

    def _helper(filename):
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        return os.path.join(
            os.path.dirname(os.path.realpath(module.__file__)),
            'data',
            filename,
        )
    return _helper


@pytest.fixture(autouse=True)
def set_caplog_level(app, caplog):
    """
    This fixture restricts the log levels that are captured by caplog for each
    funciton. Unfortunately, caplog can only be consumed by other function
    scoped fixtures. So, for exaple, if the config file sets the log level
    to 'INFO' and there are any 'DEBUG' log lines in code that is executed
    in fixtures with a wider scope than function, those will appear in the
    caplog.

    .. note:: This doesn't seem to work at all
    """
    caplog.set_level(getattr(logging, app.config['LOGGER_LEVEL']))


@pytest.yield_fixture(scope='session')
def app():
    """
    A fixture that provides an app throughout the entire test run session
    """
    test_config_file = os.environ.get('TEST_CONFIG_FILE') or 'etc/test.json'
    test_config = HexConfig.load_config(test_config_file)
    app = create_app(test_config)
    context = app.app_context()
    context.push()
    yield app
    context.pop()


@pytest.yield_fixture(autouse=True)
def function_set_up(app, request):
    with app.app_context():
        db.session.begin_nested()
        yield
        db.session.rollback()


@pytest.yield_fixture(scope="session", autouse=True)
def session_set_up(app, request):
    """
    A testing fixture for an entire test session. This fixture will gurantee
    that the database is empty at the beginning of the test session. It will
    be used automatically
    """
    with app.app_context():
        db.drop_all()
        db.session.commit()
        db.create_all()
        create_default_data()
        db.session.commit()
        yield
        db.drop_all()
        db.session.commit()