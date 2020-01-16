from smtplib import SMTPException
from unittest import mock


from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class SendPasswordResetEmailTestCaseMixin:
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            email="foo@email.com", username="foo@email.com", is_active=False
        )
        self.user1.set_password("fh39fh3344o")
        self.user1.save()
        self.user1 = get_user_model().objects.create(
            email="bar@email.com", username="bar@email.com", is_active=True
        )
        self.user1.set_password("fh39fh3344o")
        self.user1.save()

    def test_send_email_invalid_email(self):
        """
        invalid email should be successful request
        """
        query = self.get_query("invalid@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

    def test_send_email_to_not_verified_user(self):
        query = self.get_query("foo@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["email"], [Messages.NOT_VERIFIED_PASSWORD_RESET]
        )

    def test_send_email_valid_email_is_active(self):
        query = self.get_query("bar@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(
            executed["errors"], None,
        )

    @mock.patch(
        "graphql_auth.mixins.SendEmailMixin.send_email",
        mock.MagicMock(side_effect=SMTPException),
    )
    def test_send_email_fail_to_send_email(self):
        """
        Something went wrong when sending email
        """
        mock
        query = self.get_query("bar@email.com")
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.EMAIL_FAIL,
        )


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
