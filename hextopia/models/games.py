from hextopia.app import db
from hextopia.models.boards import Board
from hextopia.constants import (
    DEFAULT_GRID_SIZE,
)


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
    def create(cls, name, board_size=DEFAULT_GRID_SIZE):
        self = cls(name=name)
        with db.session.begin_nested():
            db.session.add(self)
        Board.create(game=self, size=board_size)
        return self
