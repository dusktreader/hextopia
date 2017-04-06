"""
Provides an application for uwsgi.
Notice that a local object named 'application' must be present
"""

from hextopia.app import create_app
from hextopia.config import HexConfig

config = HexConfig.load_config()
config['LOGGER_FILE_NAME'] = 'cem-api'
application = create_app(config)


if __name__ == '__main__':
    application.run()
