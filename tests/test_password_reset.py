from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages
from graphql_auth.utils import get_token, get_token_paylod


class PasswordResetTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="gaa@email.com", username="gaa", verified=True, archived=False
        )
        self.user1_old_pass = self.user1.password

    def test_reset_password(self):
        token = get_token(self.user1, "password_reset")
        query = self.get_query(token)
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user1.refresh_from_db()
        self.assertFalse(self.user1_old_pass == self.user1.password)

    def test_reset_password_invalid_form(self):
        token = get_token(self.user1, "password_reset")
        query = self.get_query(token, "wrong_pass")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])
        self.user1.refresh_from_db()
        self.assertFalse(self.user1_old_pass != self.user1.password)

    def test_reset_password_invalid_token(self):
        query = self.get_query("fake_token")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["nonFieldErrors"])
        self.user1.refresh_from_db()
        self.assertTrue(self.user1_old_pass == self.user1.password)

    def test_revoke_refresh_tokens_on_password_reset(self):
        executed = self.make_request(self.get_login_query())
        self.user1.refresh_from_db()
        refresh_tokens = self.user1.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertFalse(token.revoked)
        token = get_token(self.user1, "password_reset")
        query = self.get_query(token)
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user1.refresh_from_db()
        self.assertFalse(self.user1_old_pass == self.user1.password)
        refresh_tokens = self.user1.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertTrue(token.revoked)

    def test_reset_password_verify_user(self):
        self.user1.verified = False
        self.user1.save()

        token = get_token(self.user1, "password_reset")
        query = self.get_query(token)
        executed = self.make_request(query)

        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user1.refresh_from_db()
        self.assertFalse(self.user1_old_pass == self.user1.password)
        self.assertTrue(self.user1.status.verified)


class PasswordResetTestCase(PasswordResetTestCaseMixin, DefaultTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                username: "foo_username",
                password: "%s",
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def get_query(
        self, token, new_password1="new_password", new_password2="new_password"
    ):
        return """
        mutation {
            passwordReset(
                token: "%s",
                newPassword1: "%s",
                newPassword2: "%s"
            )
            { success, errors }
        }
        """ % (
            token,
            new_password1,
            new_password2,
        )


class PasswordResetRelayTestCase(PasswordResetTestCaseMixin, RelayTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                input: {
                    username: "foo_username",
                    password: "%s",
                }
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def get_query(
        self, token, new_password1="new_password", new_password2="new_password"
    ):
        return """
        mutation {
            passwordReset(
                input: {
                    token: "%s",
                    newPassword1: "%s",
                    newPassword2: "%s"
                })
            { success, errors }
        }
        """ % (
            token,
            new_password1,
            new_password2,
        )
