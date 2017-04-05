from collections import namedtuple

from hextopia.exceptions import HexError
from hextopia.constants import (
    DEFAULT_GRID_SIZE,
)


Coords = namedtuple('Coords', ['a', 'b'])


class HexGrid:

    def __init__(self, size=DEFAULT_GRID_SIZE):
        self.size = size

    def contains(self, coords):
        if coords.a * coords.b > 0:
            return abs(coords.a) + abs(coords.b) < self.size
        else:
            return abs(coords.a) < self.size and abs(coords.b) < self.size

    def immediate_neighbors(self, coords):
        HexError.require_condition(
            self.contains(coords),
            "coords ({}, {}) are outside the grid bounds",
            coords.a, coords.b,
        )
        neighbors = [
            Coords(coords.a + 0, coords.b - 1),
            Coords(coords.a + 1, coords.b - 1),
            Coords(coords.a + 1, coords.b + 0),
            Coords(coords.a + 0, coords.b + 1),
            Coords(coords.a - 1, coords.b + 1),
            Coords(coords.a - 1, coords.b + 0),
        ]
        return [n for n in neighbors if self.contains(n)]

    def neighborhood(self, coords, radius):
        HexError.require_condition(
            self.contains(coords),
            "coords ({}, {}) are outside the grid bounds",
            coords.a, coords.b,
        )

        HexError.require_condition(
            radius > 0,
            "radius must be a positive integer",
        )
        current_radius = 0
        neighborhood = {}
        pending = {coords: current_radius}
        while len(pending) > 0:
            for c in list(pending.keys()):
                r = pending.pop(c)
                neighborhood[c] = r
                if r < radius:
                    for n in self.immediate_neighbors(c):
                        if n not in pending and n not in neighborhood:
                            pending[n] = r + 1
        return neighborhood
