from smtplib import SMTPException
from unittest import mock


from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class SendPasswordResetEmailTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="foo@email.com", username="foo", verified=False
        )
        self.user2 = self.register_user(
            email="bar@email.com",
            username="bar",
            verified=True,
            secondary_email="secondary@email.com",
        )

    def test_send_email_invalid_email(self):
        """
        invalid email should be successful request
        """
        query = self.get_query("invalid@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

    def test_invalid_form(self):
        query = self.get_query("baremail.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["email"])

    def test_send_email_valid_email_verified_user(self):
        query = self.get_query("bar@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

    def test_send_to_secondary_email(self):
        query = self.get_query("secondary@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

    @mock.patch(
        "graphql_auth.models.UserStatus.send_password_reset_email",
        mock.MagicMock(side_effect=SMTPException),
    )
    def test_send_email_fail_to_send_email(self):
        mock
        query = self.get_query("bar@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.EMAIL_FAIL)


class SendPasswordResetEmailTestCase(
    SendPasswordResetEmailTestCaseMixin, DefaultTestCase
):
    def get_query(self, email):
        return """
        mutation {
        sendPasswordResetEmail(email: "%s")
            { success, errors }
        }
        """ % (
            email
        )


class SendPasswordResetEmailRelayTestCase(
    SendPasswordResetEmailTestCaseMixin, RelayTestCase
):
    def get_query(self, email):
        return """
        mutation {
        sendPasswordResetEmail(input:{ email: "%s"})
            { success, errors  }
        }
        """ % (
            email
        )
