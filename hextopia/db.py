import flask_sqlalchemy

"""
HERE BE DRAGONS
Basically, there is no good way to configure flask-sqlalchemy to accept our
__tablename__ classproperty for our base model as the method for generating
the table name for our models while still having a primary key on the model.
I've brought up the problem in an issue here:
https://github.com/mitsuhiko/flask-sqlalchemy/issues/428
Until this issue is addressed somehow, we can simply force flask-sqlalchemy
to not use it's automatic tablename generation
"""
flask_sqlalchemy._should_set_tablename = lambda bases, d: False


class HexAlchemy(flask_sqlalchemy.SQLAlchemy):

    def safe_commit(self, *args, **kwargs):
        """
        Commits a database transaction to the database. Because tests use
        nested sessions to create savepoints, this commit method needs to check
        if the current app is being used in testing mode. In such a case, the
        method is an effective no-op. This method should be preferred in the
        cem code base to calling db.session.commit directly.
        """
        if not self.get_app().config.get('TESTING'):
            self.session.commit(*args, **kwargs)
