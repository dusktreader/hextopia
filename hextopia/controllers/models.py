from hextopia.exceptions import InstanceNotFound


class ModelController:
    """
    Provides a simple controller that offers CRUD operations for a model
    """

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        return self.model.create(**kwargs).serialize()

    def read(self, id):
        return self._get_instance(id).serialize()

    def update(self, id, **kwargs):
        return self._get_instance(id).update(**kwargs).serialze()

    def delete(self, id):
        return self._get_instance(id).delete()

    def _get_instance(self, id):
        instance = self.model.query.get(id)
        InstanceNotFound.require_condition(
            instance is not None, self.model, id,
        )
        return instance
