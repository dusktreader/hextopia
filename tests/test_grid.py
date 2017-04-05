import pytest

from hextopia.grid import HexGrid, Coords
from hextopia.exceptions import HexError


class TestHexGrid:

    def test_check_coords(self):
        grid = HexGrid(size=3)

        assert grid.contains(Coords(a=2, b=-2))
        assert grid.contains(Coords(a=0, b=2))
        assert grid.contains(Coords(a=-2, b=2))
        assert grid.contains(Coords(a=-2, b=0))
        assert grid.contains(Coords(a=0, b=-2))

        assert not grid.contains(Coords(a=-2, b=-2))
        assert not grid.contains(Coords(a=2, b=2))
        assert not grid.contains(Coords(a=3, b=0))
        assert not grid.contains(Coords(a=0, b=-3))
        assert not grid.contains(Coords(a=2, b=-3))

    def test_immediate_neighbors(self):
        grid = HexGrid(size=3)

        assert grid.immediate_neighbors(Coords(a=0, b=0)) == [
            Coords(+0, -1),
            Coords(+1, -1),
            Coords(+1, +0),
            Coords(+0, +1),
            Coords(-1, +1),
            Coords(-1, +0),
        ]

        assert grid.immediate_neighbors(Coords(a=-1, b=+1)) == [
            Coords(-1, +0),
            Coords(+0, +0),
            Coords(+0, +1),
            Coords(-1, +2),
            Coords(-2, +2),
            Coords(-2, +1),
        ]

        assert grid.immediate_neighbors(Coords(a=-1, b=-1)) == [
            Coords(+0, -2),
            Coords(+0, -1),
            Coords(-1, +0),
            Coords(-2, +0),
        ]

        assert grid.immediate_neighbors(Coords(a=+0, b=+2)) == [
            Coords(+0, +1),
            Coords(+1, +1),
            Coords(-1, +2),
        ]

    def test_neighborhood(self):
        grid = HexGrid(size=4)

        assert grid.neighborhood(Coords(a=0, b=0), 2) == {
            Coords(-2, +0): 2,
            Coords(-1, -1): 2,
            Coords(+0, -2): 2,
            Coords(+1, -2): 2,
            Coords(+2, -2): 2,
            Coords(+2, -1): 2,
            Coords(+2, +0): 2,
            Coords(+1, +1): 2,
            Coords(+0, +2): 2,
            Coords(-1, +2): 2,
            Coords(-2, +2): 2,
            Coords(-2, +1): 2,

            Coords(-1, +0): 1,
            Coords(+0, -1): 1,
            Coords(+1, -1): 1,
            Coords(+1, +0): 1,
            Coords(+0, +1): 1,
            Coords(-1, +1): 1,

            Coords(+0, +0): 0,
        }

        grid = HexGrid(size=3)
        assert grid.neighborhood(Coords(a=+2, b=-1), 2) == {
            Coords(+0, -1): 2,
            Coords(+1, -2): 2,
            Coords(+1, +1): 2,
            Coords(+0, +1): 2,
            Coords(+0, +0): 2,

            Coords(+1, -1): 1,
            Coords(+2, -2): 1,
            Coords(+2, +0): 1,
            Coords(+1, +0): 1,

            Coords(+2, -1): 0,
        }
