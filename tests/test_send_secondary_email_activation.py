from smtplib import SMTPException
from unittest import mock

from .testCases import RelayTestCase, DefaultTestCase


class SendSecondaryEmailActivationTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="gaa@email.com", username="gaa", verified=False
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True
        )

    def test_not_verified_user(self):
        variables = {"user": self.user1}
        executed = self.make_request(self.get_query("gaa@email.com"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])

    def test_invalid_email(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query("invalidm"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])

    def test_used_email(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query("gaa@email.com"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])

    def test_valid_email(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query("new_email@email.com"), variables)
        self.assertEqual(executed["success"], True)
        self.assertFalse(executed["errors"])

    @mock.patch(
        "graphql_auth.models.UserStatus.send_secondary_email_activation",
        mock.MagicMock(side_effect=SMTPException),
    )
    def test_resend_email_fail_to_send_email(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query("new_email@email.com"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])


class SendSecondaryEmailActivationTestCase(
    SendSecondaryEmailActivationTestCaseMixin, DefaultTestCase
):
    def get_query(self, email, password=None):
        return """
        mutation {
        sendSecondaryEmailActivation(email: "%s", password: "%s")
            { success, errors }
        }
        """ % (
            email,
            password or self.default_password,
        )


class SendSecondaryEmailActivationRelayTestCase(
    SendSecondaryEmailActivationTestCaseMixin, RelayTestCase
):
    def get_query(self, email, password=None):
        return """
        mutation {
        sendSecondaryEmailActivation(input:{ email: "%s", password: "%s"})
            { success, errors  }
        }
        """ % (
            email,
            password or self.default_password,
        )
