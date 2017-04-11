from hextopia.resources import HexResource
from hextopia.app import api
from hextopia.models.games import Game

from hextopia.controllers.models import ModelController

games_ns = api.namespace('games', description='Game interface', path='/api/sources')
sources_api_model = api.model('Game', Game.serialized_model)


class GameResource(HexResource):

    _controller = ModelController(Game)

    @games_ns.response(200, 'Found and retrieved instance')
    @games_ns.response(204, 'Instance not found')
    def get(self, id):
        return super().get(id)

    @games_ns.expect(sources_api_model)
    @games_ns.response(202, 'Update accepted.')
    @games_ns.response(204, 'Instance not found')
    def put(self, id):
        return super().put(id)

    @games_ns.response(202, 'Instance deleted')
    @games_ns.response(204, 'Instance not found')
    def delete(self, id):
        return super().delete(id)

    @games_ns.expect(sources_api_model)
    @games_ns.response(201, 'Object successfully created.')
    def post(self):
        return super().post()
