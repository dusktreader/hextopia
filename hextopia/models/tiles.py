import textwrap

from sqlalchemy.ext.hybrid import hybrid_property

from hextopia.app import db


class Tile(db.Model):

    __tablename__ = 'tiles'

    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(
        db.Integer,
        db.ForeignKey('boards.id'),
        index=True,
        nullable=False,
    )

    # Look into custom types
    coords = db.Column(db.ARRAY(db.Integer), index=True)

    # Terrain, units, etc...
    current_unit_id = db.Column(
        db.Integer,
        db.ForeignKey('units.id'),
    )
    current_terrain_id = db.Column(
        db.Integer,
        db.ForeignKey('units.id'),
        nullable=False,
    )

    board = db.relationship('Board', back_populates='tiles')

    @hybrid_property
    def a(self):
        return self.coords[0]

    @a.expression
    def a(cls):
        """
        This is necessary because postgres uses 1-based indexing for arrays
        """
        return Tile.coords[1]

    @hybrid_property
    def b(self):
        return self.coords[1]

    @b.expression
    def b(cls):
        """
        This is necessary because postgres uses 1-based indexing for arrays
        """
        return Tile.coords[2]

    @classmethod
    def create(cls, board, coords):
        self = cls(
            board=board,
            coords=list(coords),
        )
        with db.session.begin_nested():
            db.session.add(self)
        return self

    def __repr__(self):
        return "{class_name} ({id})".format(
            class_name=self.__class__.__name__,
            id=self.id,
        )

    def __str__(self):
        return textwrap.dedent(
            """
                {}:
                    board: {},
                    coords: {},
                    a: {},
                    b: {},
            """.format(
                repr(self),
                self.board.id,
                self.coords,
                self.a,
                self.b,
            )
        )
