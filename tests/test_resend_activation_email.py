from smtplib import SMTPException
from unittest import mock

from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class ResendActivationEmailTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="gaa@email.com", username="gaa", verified=False
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True
        )

    def test_resend_email_invalid_email(self):
        """
        invalid email should be successful request
        """
        query = self.get_query("invalid@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

    def test_resend_email_valid_email(self):
        query = self.get_query("gaa@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

    def test_resend_email_valid_email_verified(self):
        query = self.get_query("bar@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["email"], Messages.ALREADY_VERIFIED)

    def test_invalid_form(self):
        query = self.get_query("baremail.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["email"])

    @mock.patch(
        "graphql_auth.models.UserStatus.resend_activation_email",
        mock.MagicMock(side_effect=SMTPException),
    )
    def test_resend_email_fail_to_send_email(self):
        """
        Something went wrong when sending email
        """
        mock
        query = self.get_query("gaa@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.EMAIL_FAIL)


class ResendActivationEmailTestCase(
    ResendActivationEmailTestCaseMixin, DefaultTestCase
):
    def get_query(self, email):
        return """
        mutation {
        resendActivationEmail(email: "%s")
            { success, errors }
        }
        """ % (
            email
        )


class ResendActivationEmailRelayTestCase(
    ResendActivationEmailTestCaseMixin, RelayTestCase
):
    def get_query(self, email):
        return """
        mutation {
        resendActivationEmail(input:{ email: "%s"})
            { success, errors  }
        }
        """ % (
            email
        )
