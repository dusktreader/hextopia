from buzz import Buzz


class HexError(Buzz):
    pass


class InstanceNotFound(HexError):
    """
    This exception provides some convenience to surround queries to look for
    specific instances. It comes with a predetermined message. The user simply
    supplies the id of the instance that could not be found
    """
    message = '{} instance not found for primary key {}'

    def __init__(self, instance_class, id):
        super().__init__(self.message, instance_class.__name__, id)

    @classmethod
    def require_condition(cls, expr, instance_class, id):
        if not expr:
            raise cls(instance_class, id)


class ModelValidationFailed(HexError):
    """
    This exception indicates that a validation of a flask_restplus api model's
    validation failed
    """
    pass


class ReadOnlyViolation(HexError):
    """
    This exception provides some convenience to surround queries that attempt
    to change read-only fields. It comes with a predetermined message. The
    user simply supplies the names of the fields that could not be updated
    because they are read-only.
    """
    message = 'fields {} are not writeable for {}'

    def __init__(self, instance_class, *forbidden_fields):
        super().__init__(
            self.message,
            forbidden_fields,
            instance_class.__name__,
        )

    @classmethod
    def require_condition(cls, expr, instance_class, *forbidden_fields):
        if not expr:
            raise cls(instance_class, *forbidden_fields)
