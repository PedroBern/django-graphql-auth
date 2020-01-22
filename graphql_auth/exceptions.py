from django.utils.translation import ugettext as _


class GraphQLAuthError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class UserAlreadyVerified(GraphQLAuthError):
    default_message = _("User already verified.")


class UserNotVerified(GraphQLAuthError):
    default_message = _("User is not verified.")


class WrongUsage(GraphQLAuthError):
    """
    internal exception
    """

    default_message = _("Wrong usage, check your code!.")
