import flask_restplus

from hextopia.misc import classproperty
from hextopia.app import db
from hextopia.models.boards import Board


class Game(db.Model):

    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False, index=True)

    board = db.relationship(
        'Board',
        uselist=False,
        back_populates='game',
    )

    @classmethod
    def create(cls, **kwargs):
        board_kwargs = {}
        for key in list(kwargs.keys()):
            if key.startswith('board_'):
                board_kwargs[key.replace('board_', '')] = kwargs.pop(key)

        self = cls(**kwargs)
        with db.session.begin_nested():
            db.session.add(self)
        Board.create(game=self, **board_kwargs)
        return self

    def update(self, **kwargs):
        return self

    def delete(self):
        try:
            with db.session.begin_nested():
                db.session.delete(self)
        except Exception as err:
            print("what the fuck, {}".format(err))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'board_id': self.board.id,
        }

    @classproperty
    def get_schema(cls):
        return {
            'id': flask_restplus.fields.Integer,
            'name': flask_restplus.fields.String,
            'board_id': flask_restplus.fields.Integer,
        }

    @classproperty
    def put_schema(cls):
        return {}

    @classproperty
    def post_schema(cls):
        return {
            'name': flask_restplus.fields.String,
            'board_size': flask_restplus.fields.Integer,
        }
