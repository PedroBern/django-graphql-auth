from django.contrib.auth import get_user_model

from graphql_jwt.refresh_token.models import RefreshToken

from .testCases import RelayTestCase, DefaultTestCase

from graphql_auth.utils import revoke_user_refresh_token
from graphql_auth.constants import Messages
from graphql_auth.utils import get_token, get_token_paylod


class PasswordChangeTestCaseMixin:
    def setUp(self):
        self.user = self.register_user(
            email="gaa@email.com", username="gaa", verified=True
        )
        self.old_pass = self.user.password

    def test_password_change(self):
        """
        change password
        """
        variables = {"user": self.user}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])
        self.user.refresh_from_db()
        self.assertFalse(self.old_pass == self.user.password)

    def test_mismatch_passwords(self):
        """
        wrong inputs
        """
        variables = {"user": self.user}
        executed = self.make_request(self.get_query("wrong"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["newPassword2"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])
        self.user.refresh_from_db()
        self.assertTrue(self.old_pass == self.user.password)

    def test_passwords_validation(self):
        """
        easy password
        """
        variables = {"user": self.user}
        executed = self.make_request(self.get_query("123", "123"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["newPassword2"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    def test_revoke_refresh_tokens_on_password_change(self):
        executed = self.make_request(self.get_login_query())
        self.user.refresh_from_db()
        refresh_tokens = self.user.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertFalse(token.revoked)
        variables = {"user": self.user}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])
        self.user.refresh_from_db()
        self.assertFalse(self.old_pass == self.user.password)
        refresh_tokens = self.user.refresh_tokens.all()
        revoke_user_refresh_token(self.user)
        self.user.refresh_from_db()
        refresh_tokens = self.user.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertTrue(token.revoked)


class PasswordChangeTestCase(PasswordChangeTestCaseMixin, DefaultTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                username: "username",
                password: "%s",
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def get_query(self, new_password1="new_password", new_password2="new_password"):
        return """
        mutation {
            passwordChange(
                oldPassword: "%s",
                newPassword1: "%s",
                newPassword2: "%s"
            )
            { success, errors, token, refreshToken }
        }
        """ % (
            self.default_password,
            new_password1,
            new_password2,
        )


class PasswordChangeRelayTestCase(PasswordChangeTestCaseMixin, RelayTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                input: {
                    username: "username",
                    password: "%s",
                }
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def get_query(self, new_password1="new_password", new_password2="new_password"):
        return """
        mutation {
            passwordChange(
                input: {
                    oldPassword: "%s",
                    newPassword1: "%s",
                    newPassword2: "%s"
                })
            { success, errors, token, refreshToken }
        }
        """ % (
            self.default_password,
            new_password1,
            new_password2,
        )
