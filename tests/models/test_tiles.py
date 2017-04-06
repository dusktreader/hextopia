from hextopia.models.tiles import Tile
from hextopia.models.games import Game


class TestTile:

    def test_coords(self):
        game = Game.create(name='test_game', board_size=3)
        assert Tile.query.filter_by(board=game.board).count() > 1
        tile = Tile.query.filter_by(board=game.board, a=2, b=-1).one_or_none()
        assert tile is not None
        assert tile.a == 2
        assert tile.b == -1
        assert tile.coords == [2, -1]
