from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages, TokenAction
from graphql_auth.utils import get_token, get_token_paylod


class PasswordResetTestCaseMixin:
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            email="foo@email.com", username="foo_username", is_active=True
        )
        self.user1.set_password("fh39fh3344o")
        self.user1.save()
        self.user1_old_pass = self.user1.password
        self.user2 = get_user_model().objects.create(
            email="bar@email.com", username="bar_username", is_active=False
        )
        self.user2.set_password("fh39fh3344o")
        self.user2.save()
        self.user2_old_pass = self.user2.password

    def test_reset_password(self):
        token = get_token(self.user1, TokenAction.PASSWORD_RESET)
        query = self.get_query(token)
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user1.refresh_from_db()
        self.assertFalse(self.user1_old_pass == self.user1.password)

    def test_reset_password_invalid_token(self):
        query = self.get_query("fake_token")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["nonFieldErrors"])
        self.user1.refresh_from_db()
        self.assertTrue(self.user1_old_pass == self.user1.password)


class PasswordResetTestCase(PasswordResetTestCaseMixin, DefaultTestCase):
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
