from hextopia.exceptions import HexError
from hextopia.constants import (
    DEFAULT_GRID_SIZE,
)


class Coords:

    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    def __iter__(self):
        yield self.a
        yield self.b

    def __getitem__(self, idx):
        if idx == 0:
            return self.a
        elif idx == 1:
            return self.b
        else:
            raise HexError("Invalid index for coords: {}", idx)

    def __str__(self):
        return "({}, {})".format(self.a, self.b)

    def __eq__(self, other):
        return self[0] == other[0] and self[1] == other[1]

    def __neg__(self):
        return self.__class__(-self[0], -self[1])

    def __add__(self, other):
        return self.__class__(self[0] + other[0], self[1] + other[1])

    def __hash__(self):
        return hash((self.a, self.b))


class HexGrid:

    def __init__(self, size=DEFAULT_GRID_SIZE):
        self.size = size

    def __iter__(self):
        for coords in self.neighborhood(Coords(0, 0), self.size).keys():
            yield coords

    def contains(self, coords):
        coords = Coords(*coords)
        if coords.a * coords.b > 0:
            return abs(coords.a) + abs(coords.b) < self.size
        else:
            return abs(coords.a) < self.size and abs(coords.b) < self.size

    def immediate_neighbors(self, coords):
        coords = Coords(*coords)
        HexError.require_condition(
            self.contains(coords),
            "coords ({}, {}) are outside the grid bounds",
            coords.a, coords.b,
        )
        neighbors = [
            coords + (+0, -1),
            coords + (+1, -1),
            coords + (+1, +0),
            coords + (+0, +1),
            coords + (-1, +1),
            coords + (-1, +0),
        ]
        return [n for n in neighbors if self.contains(n)]

    def neighborhood(self, coords, radius):
        coords = Coords(*coords)
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
