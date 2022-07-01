class CloudException(Exception):
    pass


class TokenException(CloudException):
    """Primary exception for errors thrown in the get token post request."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")


class GetException(CloudException):
    """Basic exception for errors thrown on get request."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")


class PostException(CloudException):
    """Basic exception for errors thrown on post request."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")


class SetSession(CloudException):
    """Base exception for errors caused within a get couriers."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")


class CheckTimeToken(CloudException):
    """Base exception for errors caused within a get couriers."""

    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")


class ParamSetException(CloudException):
    """"""
    def __init__(self, name_class, name_method, message):
        super().__init__(f"Class: \"{name_class}\", Method: \"{name_method}\", Message: {message}")