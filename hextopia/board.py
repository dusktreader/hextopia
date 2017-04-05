from hextopia.grid import HexGrid
from hextopia.exceptions import HexError
from hextopia.constants import (
    DEFAULT_GRID_SIZE,
)


class Tile:
    pass


class Board:

    def __init__(self, size=DEFAULT_GRID_SIZE):
        self.grid = HexGrid(size=size)
        self.tiles = {}

    def get_tile(self, coords):
        HexError.require_condition(
            self.grid.contains(coords),
            "coords are not within grid: {}",
            coords,
        )
        return self.tiles.setdefault(coords, Tile())

    def __iter__(self):
        for coords in self.grid:
            yield self.get_tile(coords)
