import logbook
import os
import sys

from hextopia.constants import (
    DEFAULT_LOGGER_NAME,
)


class HexLogger(logbook.Logger):

    def __init__(self, *args, app=None, **kwargs):
        """
        Initializes the logger in the manner of a common flask extension
        """
        super().__init__(*args, **kwargs)
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        """
        Initializes this logger in the manner of a standard flask extension.
        Initializes all of the handlers based on application configuration
        """
        self.app = app

        self.remove_all_flask_handlers()
        self.replace_flask_logger()

        self._setup_default_handler()
        self._setup_file_handler()
        self._setup_test_handler()

        self.info("{} logger initialized with flask app", self.name)

    def _setup_default_handler(self):
        """
        This helper method sets up the default logging which just prints to
        stderr. If the application is currently in TESTING mode, it is not
        activated because the logged messages will be captured by the
        test_handler
        """
        testing_flag = self.app.config.get('TESTING')
        if testing_flag:
            return

        level_name = self.app.config.get('LOGGER_LEVEL', 'INFO')

        logbook.StreamHandler(
            sys.stderr,
            level=logbook.lookup_level(level_name),
            bubble=True,
            format_string=self.app.config.get('LOGGER_FORMAT'),
        ).push_application()

    def _setup_test_handler(self):
        """
        This helper method sets up the test logging adapter which captures
        log messages in memory when the application is in TESTING mode. It will
        use the NOTSET level so that all log messages are captured. Also note
        that bubble is not set, so the log messages should not bubble up past
        this handler
        """
        testing_flag = self.app.config.get('TESTING')
        if not testing_flag:
            return

        logbook.TestHandler(
            level=logbook.NOTSET,
        ).push_application()

    def _setup_file_handler(self):
        """
        This helper method sets up a rotating file logger based on the base
        path supplied in the configuration. No file logging is performed if
        the base path is not supplied
        """
        log_path_base = self.app.config.get('LOGGER_PATH_BASE')
        if log_path_base is None:
            return

        log_path_base = os.path.expanduser(log_path_base)
        if not os.path.exists(log_path_base):
            os.makedirs(log_path_base)

        log_file_name = self.app.config.get('LOGGER_FILE_NAME')
        if log_file_name is None:
            log_file_name = os.path.basename(sys.argv[0])

        level_name = self.app.config.get('LOGGER_LEVEL', 'INFO')

        logbook.RotatingFileHandler(
            os.path.join(log_path_base, log_file_name + '.log'),
            level=logbook.lookup_level(level_name),
            bubble=True,
            format_string=self.app.config.get('LOGGER_FORMAT'),
        ).push_application()

    def remove_all_flask_handlers(self):
        """
        This method just removes all the native flask logging handlers. These
        are not very helpful as is, and may be removed from future versions
        of flask:
        https://github.com/pallets/flask/issues/2023
        """
        for handler in list(self.app.logger.handlers):
            self.app.logger.removeHandler(handler)

    def replace_flask_logger(self):
        """
        This method replaces flask's logger with this CEM logger
        """
        self.app._logger = self
        self.app._logger_name = self.name
