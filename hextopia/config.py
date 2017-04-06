import os
import sys
import pydon

from hextopia.exceptions import HexError
from hextopia.constants import (
    DEFAULT_CONFIG_FILE,
    CONFIG_FILE_ENV_VAR,
)


class HexConfig(dict):
    """
    This is a specialized class for configs.
    It adds the following functionality:
    * validation and uri interpolation in the finalize method
    * add command line arguments for config file selection
    """

    def __getattr__(self, key):
        return super().get(key)

    def __setattr__(self, key, value):
        return super().__setitem__(key, value)

    def __str__(self):
        return '\n    '.join(
            ['{} Configuration'.format(self.NAME)] +
            ['{}: {}'.format(k, self[k]) for k in sorted(self.keys())]
        )

    def _finalize_email_logger(self):
        if self.LOGGER_EMAIL:
            for key in ['LEVEL', 'FROM_ADDR', 'TO_ADDR', 'SUBJECT']:
                full_key = 'LOGGER_EMAIL_' + key
                HexError.require_condition(
                    self.get(full_key),
                    "{} is required when LOGGER_EMAIL is set",
                    full_key,
                )

    def _finalize_profiler(self):
        if self.PROFILE:
            if self.PROFILE_DIR:
                self.PROFILE_DIR = os.path.expanduser(self.PROFILE_DIR)
                with HexError.handle_errors(
                        "PROFILE_DIR invalid or nonextant: {}",
                        self.PROFILE_DIR,
                ):
                    if not os.path.exists(self.PROFILE_DIR):
                        os.makedirs(os.path.abspath(self.PROFILE_DIR))

    def _finalize_db_uri(self):
        self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URI_FORMAT.format(
            dialect=self.DATABASE_DIALECT,
            driver=self.DATABASE_DRIVER,
            username=self.DATABASE_USERNAME,
            password=self.DATABASE_PASSWORD,
            server=self.DATABASE_SERVER,
            port=self.DATABASE_PORT,
            name=self.DATABASE_NAME,
        )

    def finalize(self):
        """
        Massages some settings in the loaded config with some validation and
        other setup
        """
        self._finalize_email_logger()
        self._finalize_profiler()
        self._finalize_db_uri()
        return self

    @classmethod
    def load_config(cls, file_path=None):
        """
        Loads a config from a file.

        :param file_path: the path to the configuration file
                          If this argument is None, then check environment
        """

        self = cls()
        self.update(pydon.load_file(DEFAULT_CONFIG_FILE))

        file_path = file_path or os.environ.get(CONFIG_FILE_ENV_VAR)
        if file_path:
            self.update(pydon.load_file(file_path))

        return self.finalize()

    def write_config(self, file_path=None, ignore_defaults=False):
        """
        Dumps this config to file our stdout.

        :param: file_path:       If specified, write config to file
        :param: remove_defaults: Don't include settings that are defaults

        """
        output = self.copy()
        if ignore_defaults:
            default_dict = pydon.load_file(DEFAULT_CONFIG_FILE)
            for key in default_dict.keys():
                if key in output and output[key] == default_dict[key]:
                    del output[key]

        if file_path is None:
            sys.stdout.write(pydon.dump_string(output, indent=4, width=1))
        else:
            pydon.dump_file(output, file_path, indent=4, width=1)
