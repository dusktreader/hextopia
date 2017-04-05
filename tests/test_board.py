from hextopia.board import Board, Tile
from hextopia.grid import Coords


class TestBoard:

    def test_get_tile(self):
        board = Board(size=3)
        assert Coords(1, 1) not in board.tiles
        target_tile = board.get_tile((1, 1))
        assert isinstance(target_tile, Tile)
        assert Coords(1, 1) in board.tiles
        assert board.tiles[Coords(1, 1)] is target_tile
