from unittest import mock
from functools import wraps


def fake_email_templates(fn):
    """
    # TODO: fix test email teplates

    for some reason, tests are not loading the email templates,
    this is a quick fix
    """

    @wraps(fn)
    @mock.patch(
        "graphql_auth.email.EmailBase.get_message",
        mock.MagicMock(return_value=("subject", "<p>message<p>", "message")),
    )
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper
