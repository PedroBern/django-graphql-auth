from django.contrib.auth import get_user_model

from django.utils import timezone

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class VerifyTokenTestCaseMixin:
    def setUp(self):
        self.user = self.register_user(
            email="foo@email.com", username="foo", verified=False
        )

    def test_verify_token(self):
        query = self.get_login_query()
        executed = self.make_request(query)
        self.assertTrue(executed["token"])

        query = self.get_verify_query(executed["token"])
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertTrue(executed["payload"])
        self.assertFalse(executed["errors"])

    def test_invalid_token(self):
        query = self.get_verify_query("invalid_token")
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertTrue(executed["errors"])
        self.assertFalse(executed["payload"])


class VerifyTokenTestCase(VerifyTokenTestCaseMixin, DefaultTestCase):
    def get_login_query(self):
        return """
        mutation {
        tokenAuth(email: "foo@email.com", password: "%s" )
            { token, success, errors  }
        }
        """ % (
            self.default_password
        )

    def get_verify_query(self, token):
        return """
        mutation {
        verifyToken(token: "%s" )
            { success, errors, payload  }
        }
        """ % (
            token
        )


class VerifyTokenRelayTestCase(VerifyTokenTestCaseMixin, RelayTestCase):
    def get_login_query(self):
        return """
        mutation {
        tokenAuth(input:{ email: "foo@email.com", password: "%s"  })
            { token, success, errors  }
        }
        """ % (
            self.default_password
        )

    def get_verify_query(self, token):
        return """
        mutation {
        verifyToken(input: {token: "%s"} )
            { success, errors, payload  }
        }
        """ % (
            token
        )
