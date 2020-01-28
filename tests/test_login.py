from django.contrib.auth import get_user_model
from pytest import mark
from .decorators import skipif_django_21
from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class LoginTestCaseMixin:
    def setUp(self):
        self.archived_user = self.register_user(
            email="gaa@email.com", username="gaa", verified=True, archived=True
        )
        self.not_verified_user = self.register_user(
            email="boo@email.com", username="boo", verified=False
        )
        self.verified_user = self.register_user(
            email="foo@email.com",
            username="foo",
            verified=True,
            secondary_email="secondary@email.com",
        )

    def test_archived_user_becomes_active_on_login(self):
        self.assertEqual(self.archived_user.status.archived, True)
        query = self.get_query("email", self.archived_user.email)
        executed = self.make_request(query)
        self.archived_user.refresh_from_db()
        self.assertEqual(self.archived_user.status.archived, False)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["errors"])
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])

    def test_login_username(self):
        query = self.get_query("username", self.verified_user.username)
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["errors"])
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])

        query = self.get_query("username", self.not_verified_user.username)
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["errors"])
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])

    def test_login_email(self):
        query = self.get_query("email", self.verified_user.email)
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["errors"])
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])

    def test_login_secondary_email(self):
        query = self.get_query("email", "secondary@email.com")
        executed = self.make_request(query)
        self.assertTrue(executed["success"])
        self.assertFalse(executed["errors"])
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])

    def test_login_wrong_credentials(self):
        query = self.get_query("username", "wrong")
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertTrue(executed["errors"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    def test_login_wrong_credentials_2(self):
        query = self.get_query("username", self.verified_user.username, "wrongpass")
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertTrue(executed["errors"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    @mark.settings_b
    @skipif_django_21()
    def test_not_verified_login_on_different_settings(self):
        query = self.get_query("username", self.not_verified_user.username)
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.NOT_VERIFIED)
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    @mark.settings_b
    @skipif_django_21()
    def test_not_verified_login_on_different_settings_wrong_pass(self):
        query = self.get_query("username", self.not_verified_user.username, "wrongpass")
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.INVALID_CREDENTIALS
        )
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])


class LoginTestCase(LoginTestCaseMixin, DefaultTestCase):
    def get_query(self, field, username, password=None):
        return """
        mutation {
        tokenAuth(%s: "%s", password: "%s" )
            { token, refreshToken, success, errors  }
        }
        """ % (
            field,
            username,
            password or self.default_password,
        )


class LoginRelayTestCase(LoginTestCaseMixin, RelayTestCase):
    def get_query(self, field, username, password=None):
        return """
        mutation {
        tokenAuth(input:{ %s: "%s", password: "%s" })
            { token, refreshToken, success, errors  }
        }
        """ % (
            field,
            username,
            password or self.default_password,
        )
