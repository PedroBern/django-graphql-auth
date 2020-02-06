from unittest import skip

from django.contrib.auth import get_user_model
from django.utils import timezone

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


# GRAPHQL_JWT = {
#     "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
# }


class RevokeTokenTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(email="foo@email.com", username="foo_username")

    def test_revoke_token(self):
        query = self.get_login_query()
        executed = self.make_request(query)
        self.assertTrue(executed["refreshToken"])

        query = self.get_revoke_query(executed["refreshToken"])
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertTrue(executed["revoked"])
        self.assertFalse(executed["errors"])

    def test_invalid_token(self):
        query = self.get_revoke_query("invalid_token")
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertTrue(executed["errors"])
        self.assertFalse(executed["revoked"])


class RevokeTokenTestCase(RevokeTokenTestCaseMixin, DefaultTestCase):
    def get_login_query(self):
        return """
        mutation {
        tokenAuth(email: "foo@email.com", password: "%s" )
            { refreshToken, success, errors  }
        }
        """ % (
            self.default_password
        )

    def get_revoke_query(self, token):
        return """
        mutation {
        revokeToken(refreshToken: "%s" )
            { success, errors, revoked  }
        }
        """ % (
            token
        )


class VerifyTokenRelayTestCase(RevokeTokenTestCaseMixin, RelayTestCase):
    def get_login_query(self):
        return """
        mutation {
        tokenAuth(input:{ email: "foo@email.com", password: "%s"  })
            { refreshToken, success, errors  }
        }
        """ % (
            self.default_password
        )

    def get_revoke_query(self, token):
        return """
        mutation {
        revokeToken(input: {refreshToken: "%s"} )
            { success, errors, revoked  }
        }
        """ % (
            token
        )
