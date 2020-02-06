from django.contrib.auth import get_user_model

from graphql_auth.constants import Messages


from .testCases import RelayTestCase, DefaultTestCase


class SwapEmailsCaseMixin:
    def setUp(self):
        self.user = self.register_user(
            email="bar@email.com",
            username="bar",
            verified=True,
            secondary_email="secondary@email.com",
        )
        self.user2 = self.register_user(
            email="baa@email.com", username="baa", verified=True
        )

    def test_swap_emails(self):
        executed = self.make_request(self.query(), {"user": self.user})
        self.assertEqual(executed["success"], True)
        self.assertFalse(executed["errors"])
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "secondary@email.com")
        self.assertEqual(self.user.status.secondary_email, "bar@email.com")

    def test_swap_emails_without_secondary_email(self):
        executed = self.make_request(self.query(), {"user": self.user2})
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.SECONDARY_EMAIL_REQUIRED
        )


class SwapEmailsCase(SwapEmailsCaseMixin, DefaultTestCase):
    def query(self, password=None):
        return """
        mutation {
            swapEmails(password: "%s")
                { success, errors }
            }
        """ % (
            password or self.default_password
        )


class SwapEmailsRelayTestCase(SwapEmailsCaseMixin, RelayTestCase):
    def query(self, password=None):
        return """
        mutation {
        swapEmails(input:{ password: "%s"})
            { success, errors  }
        }
        """ % (
            password or self.default_password
        )
