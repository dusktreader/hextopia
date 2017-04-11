from hextopia.resources import HexResource
from hextopia.app import api
from hextopia.models.games import Game

from hextopia.controllers.models import ModelController

games_namespace = api.namespace(
    'games',
    description='Game interface',
    path='/api/games',
)


@games_namespace.route('/<int:id>', endpoint='games_instance')
@games_namespace.param('id', 'An Entity Link ID')
@games_namespace.route('', endpoint='games_post')
class GameResource(HexResource):

    _controller = ModelController(Game)

    @games_namespace.response(200, 'Found and retrieved instance')
    @games_namespace.response(204, 'Instance not found')
    def get(self, id):
        return super().get(id)

    @games_namespace.expect(api.model('GamePut', Game.put_schema))
    @games_namespace.response(202, 'Update accepted.')
    @games_namespace.response(204, 'Instance not found')
    def put(self, id):
        return super().put(id)

    @games_namespace.response(202, 'Instance deleted')
    @games_namespace.response(204, 'Instance not found')
    def delete(self, id):
        return super().delete(id)

    # @games_namespace.expect(api.model('GamePost', Game.post_schema))
    @games_namespace.response(201, 'Object successfully created.')
    def post(self):
        return super().post()
