from collections import namedtuple

from hextopia.exceptions import HexError
from hextopia.constants import (
    DEFAULT_GRID_SIZE,
)


Coords = namedtuple('Coords', ['x', 'y'])


class HexGrid:

    def __init__(self, size=DEFAULT_GRID_SIZE):
        self.size = size

    def check_coords(self, coords):
        HexError.require_condition(
            0 <= coords.x < self.size and 0 <= coords.y < self.size,
            "coords ({}, {}) are outside the grid bounds",
            self.x, self.y,
        )

    def check_index(self, idx):
        HexError.require_condition(
            0 <= idx < self.size,
            "index [{}] is outside the grid bounds",
            self.idx,
        )

    def coords(self, idx):
        """
        Returns the coordinate pair for a given index
        """
        self.check_index(idx)
        x = idx % self.size
        y = idx // self.size
        return Coords(x, y)


    def neighbors(self, coords):
        """
        Returns the six immmediate neighbors for a particular coordinate pair

        given a coordiate

          x x x x x x x x x
         x x x x X X x x x x
        x x x x X O X x x x x
         x x x x X X x x x x
          x x x x x x x x x

         a b
        c O d
         e f
        """
        hoods = [
            Coords(coords.x, (coords.y - 1) % self.size),
            Coords(coords.x, (coords.y - 1) % self.size),


