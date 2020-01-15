from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages
from graphql_auth.utils import get_token, get_token_paylod


class PasswordChangeTestCaseMixin:
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="gaa@email.com", username="username", is_active=True
        )
        self.user.set_password("aksdhaksda435")
        self.user.save()
        self.old_pass = self.user.password

    def test_password_change(self):
        """
        change password
        """
        variables = {"user": self.user}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user.refresh_from_db()
        self.assertFalse(self.old_pass == self.user.password)

    def test_mismatch_passwords(self):
        """
        wrong inputs
        """
        variables = {"user": self.user}
        executed = self.make_request(self.get_query("wrong"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["newPassword2"],)
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


class PasswordChangeTestCase(PasswordChangeTestCaseMixin, DefaultTestCase):
    def get_query(
        self, new_password1="new_password", new_password2="new_password"
    ):
        return """
        mutation {
            passwordChange(
                oldPassword: "aksdhaksda435",
                newPassword1: "%s",
                newPassword2: "%s"
            )
            { success, errors }
        }
        """ % (
            new_password1,
            new_password2,
        )


class PasswordChangeRelayTestCase(PasswordChangeTestCaseMixin, RelayTestCase):
    def get_query(
        self, new_password1="new_password", new_password2="new_password"
    ):
        return """
        mutation {
            passwordChange(
                input: {
                    oldPassword: "aksdhaksda435",
                    newPassword1: "%s",
                    newPassword2: "%s"
                })
            { success, errors }
        }
        """ % (
            new_password1,
            new_password2,
        )
