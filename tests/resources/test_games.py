import flask

from hextopia.models.games import Game

# Must be imported for the route to be set up correctly
from hextopia.resources.games import GameResource  # noqa


class TestGameResource:

    def test_get(self, client):
        Game.create(id=1, name='test_dummy', board_id=11, board_size=3)

        response = client.get(flask.url_for('games_instance', id=1))
        assert response.status_code == 200
        assert response.json == {'id': 1, 'name': 'test_dummy', 'board_id': 11}

    def test_put(self, client):
        Game.create(id=1, name='test_dummy', board_id=11, board_size=3)

        response = client.put(
            flask.url_for('games_instance', id=1),
            data=flask.json.dumps({'foo': 'bar'}),
            content_type='application/json',
        )
        assert response.status_code == 202
        assert response.json == {'id': 1, 'name': 'test_dummy', 'board_id': 11}

    def test_post(self, client):
        response = client.post(
            flask.url_for('games_post'),
            data=flask.json.dumps(
                {'id': 1, 'name': 'test_dummy', 'board_id': 11}
            ),
            content_type='application/json',
        )
        assert response.status_code == 201
        assert response.json == {'id': 1, 'name': 'test_dummy', 'board_id': 11}

    def test_delete(self, client):
        Game.create(id=1, name='test_dummy', board_id=11, board_size=3)
        assert Game.query.get(1) is not None
        response = client.delete(flask.url_for('games_instance', id=0))
        assert response.status_code == 203
        assert Game.query.get(1) is None
