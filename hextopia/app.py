import flask
import flask_migrate
import pprintpp
import werkzeug.contrib.profiler

from hextopia.logger import HexLogger
from hextopia.db import HexAlchemy


logger = HexLogger()
db = HexAlchemy()
migrator = flask_migrate.Migrate()


def create_app(config):
    """
    App factory for the hextopia api app.
    Creates new app using a config. Additionally initializes the logger, db,
    and migrator components with the newly manufactured app

    :param config: A config object. Should be duck-typed as a dict
    """

    pprintpp.monkeypatch()

    # This needs to be done here because of flask goofiness
    # import hextopia.routes  # noqa
    app = flask.Flask('hextopia')
    app.config.from_mapping(**config)
    logger.init_app(app)
    logger.debug("Manufacturing app with config: {}", str(config))

    if app.config.get('PROFILE'):
        app.wsgi_app = werkzeug.contrib.profiler.ProfilerMiddleware(
            app.wsgi_app,
            restrictions=[30],
            profile_dir=app.config.get('PROFILE_DIR'),
        )

    logger.debug("Initializing database driver")
    db.init_app(app)

    logger.debug("Initializing migrator")
    migrator.init_app(app=app, db=db, logger=logger, directory='etc/alembic')

    logger.debug("Finished creating app")
    return app
