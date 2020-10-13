from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages
from graphql_auth.utils import get_token, get_token_paylod
from graphql_auth.models import UserStatus
from graphql_auth.signals import user_verified


class VerifyAccountCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="foo@email.com", username="foo", verified=False
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True
        )

    def test_verify_user(self):
        signal_received = False

        def receive_signal(sender, user, signal):
            self.assertEqual(user.id, self.user1.id)
            nonlocal signal_received
            signal_received = True

        user_verified.connect(receive_signal)
        token = get_token(self.user1, "activation")
        executed = self.make_request(self.verify_query(token))
        self.assertEqual(executed["success"], True)
        self.assertFalse(executed["errors"])
        self.assertTrue(signal_received)

    def test_verified_user(self):
        token = get_token(self.user2, "activation")
        executed = self.make_request(self.verify_query(token))
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.ALREADY_VERIFIED
        )

    def test_invalid_token(self):
        executed = self.make_request(self.verify_query("faketoken"))
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.INVALID_TOKEN)

    def test_other_token(self):
        token = get_token(self.user2, "password_reset")
        executed = self.make_request(self.verify_query(token))
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.INVALID_TOKEN)


class VerifyAccountCase(VerifyAccountCaseMixin, DefaultTestCase):
    def verify_query(self, token):
        return """
        mutation {
            verifyAccount(token: "%s")
                { success, errors }
            }
        """ % (
            token
        )


class VerifyAccountRelayTestCase(VerifyAccountCaseMixin, RelayTestCase):
    def verify_query(self, token):
        return """
        mutation {
        verifyAccount(input:{ token: "%s"})
            { success, errors  }
        }
        """ % (
            token
        )
