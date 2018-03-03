from hextopia.models.tiles import Tile
from hextopia.models.games import Game
from hextopia.grid import HexGrid


class TestBoard:

    def test_create(self):
        game = Game.create(name='test_game', board_size=3)
        board = game.board
        assert board.game is game
        assert Tile.query.filter_by(board=board).count() == HexGrid.area(board.size)

    def test_tile(self):
        game = Game.create(name='test_game', board_size=3)
        board = game.board
        assert Tile.query.filter_by(board=board, a=2, b=-1).one() is board.tile((2, -1))
