class GraphQLAuthError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super().__init__(message)


class UserAlreadyVerified(GraphQLAuthError):
    default_message = "User already verified."


class UserNotVerified(GraphQLAuthError):
    default_message = "User is not verified."


# class VerificationRequired(GraphQLAuthError):
#     default_message = "You need to verifiy your account to perform this action."
#
#
# class FailPasswordConfirmation(GraphQLAuthError):
#     default_message = "Invalid credentials."
