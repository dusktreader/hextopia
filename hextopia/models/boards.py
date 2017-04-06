from hextopia.app import db
from hextopia.grid import Coords
from hextopia.grid import HexGrid
from hextopia.exceptions import HexError
from hextopia.models.tiles import Tile
from hextopia.constants import (
    DEFAULT_GRID_SIZE,
)


class Board(db.Model):

    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    game_id = db.Column(
        db.Integer,
        db.ForeignKey('games.id'),
        index=True,
        nullable=False,
    )

    game = db.relationship(
        'Game',
        back_populates='board',
    )

    tiles = db.relationship(
        'Tile',
        back_populates='board',
    )

    @classmethod
    def create(cls, game, size=DEFAULT_GRID_SIZE):
        self = cls(
            game=game,
            size=size,
        )
        with db.session.begin_nested():
            db.session.add(self)
        for coords in self.grid:
            Tile.create(self, coords)
        return self

    @property
    def grid(self):
        if not hasattr(self, '_grid'):
            self._grid = HexGrid(size=self.size)
        return self._grid

    def tile(self, coords):
        coords = Coords(*coords)
        HexError.require_condition(
            self.grid.contains(coords),
            "coords are not within grid: {}",
            coords,
        )
        tile = Tile.query.filter_by(
            board=self, a=coords.a, b=coords.b
        ).one_or_none()
        HexError.require_condition(
            tile is not None,
            "No tile is defined at those coords (should not happen): {}",
            coords,
        )
        return tile

    def __iter__(self):
        for coords in self.grid:
            yield self.tile(coords)
