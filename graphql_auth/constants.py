class Messages:
    INVALID_PASSWORD = [
        {"message": "Invalid password.", "code": "invalid_password",}
    ]
    UNAUTHENTICATED = [
        {"message": "Unauthenticated.", "code": "unauthenticated",}
    ]
    INVALID_TOKEN = [
        {"message": "Invalid or expirated token.", "code": "invalid_token",}
    ]
    ALREADY_VERIFIED = [
        {"message": "Account already verified.", "code": "already_verified",}
    ]
    EMAIL_FAIL = [{"message": "Failed to send email.", "code": "email_fail"}]
    INVALID_CREDENTIALS = [
        {
            "message": "Please, enter valid credentials.",
            "code": "invalid_credentials",
        }
    ]
    NOT_VERIFIED = [
        {"message": "Please verify your account.", "code": "not_verified",}
    ]
    NOT_VERIFIED_PASSWORD_RESET = [
        {
            "message": "Please verify your account before requesting the password reset.",
            "code": "not_verified",
        }
    ]


class TokenAction:
    ACTIVATION = "activation"
    PASSWORD_RESET = "password_reset"
