import flask
import flask_restplus

from hextopia.app import logger, db
from hextopia.misc import classproperty
from hextopia.exceptions import (
    HexError,
    InstanceNotFound,
    ReadOnlyViolation,
)


class HexResource(flask_restplus.Resource):

    _controller = None

    @classproperty
    def controller(cls):
        """
        .. note:: We can't use abc.ABCMeta for this because it causes conflicts
                  with the metaclass used for the Resource base. Thus, we have
                  to create a pseudo-abstract class in this manner
        """
        HexError.require_condition(
            cls._controller is not None,
            "Derived classes must set the _controller attribute",
        )
        return cls._controller

    def get(self, id):
        """
        Handles GET request

        Retrieves the single instance carrying the id provided by the parameter
        """
        try:
            return self.controller.read(id)
        except InstanceNotFound as err:
            logger.debug(err)
            return {'message': err.message}, 204
        except HexError as err:
            logger.debug(err)
            return {'message': err.message}, 400

    def put(self, id):
        """
        Handles PUT request

        Updates the single instance carrying the id provided by the parameter
        """

        try:
            logger.debug("Unpacking PUT payload")
            json = flask.request.get_json()
            HexError.require_condition(
                json is not None,
                """
                Malformed PUT request:
                Make sure header contains Content-Type=application/json
                """,
            )

            logger.debug("Updating instance")
            response = self.controller.update(id, **json)
            logger.debug("Committing change")
            db.safe_commit()
            return (response, 202)
        except InstanceNotFound as err:
            logger.debug(err)
            return {'message': err.message}, 204
        except ReadOnlyViolation as err:
            logger.debug(err)
            return {'message': err.message}, 403
        except HexError as err:
            logger.debug(err)
            return {'message': err.message}, 400

    def delete(self, id):
        """
        Handles DELETE request

        Deletes the single instance carrying the id provided by the parameter
        """
        try:
            logger.debug("Deleting instance")
            self.controller.delete(id)
            logger.debug("Committing change")
            db.safe_commit()
            return ({'message': 'Successfully deleted {}'.format(id)}, 202)
        except InstanceNotFound as err:
            logger.debug(err)
            return {'message': err.message}, 204

    def post(self):
        """
        Handles POST request

        Creates a new instance from the supplied json payload of the request.
        """
        try:
            logger.debug("Unpacking POST payload")
            json = flask.request.get_json()
            HexError.require_condition(
                json is not None,
                """
                Malformed POST request.
                Make sure header contains Content-Type=application/json
                """,
            )
            logger.debug("Creating instance")
            response = self.controller.create(**json)
            logger.debug("Committing change")
            db.safe_commit()
            return (response, 201)
        except HexError as err:
            logger.debug(err)
            return {'message': err.message}, 400
