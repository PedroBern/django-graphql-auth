from smtplib import SMTPException
from unittest import mock

from pytest import mark

from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from .decorators import skipif_django_21

from graphql_auth.constants import Messages
from graphql_auth.signals import user_registered
from graphql_auth.utils import get_token, get_token_paylod


class RegisterTestCaseMixin:
    def test_register_invalid_password_validation(self):
        """
        fail to register same user with bad password
        """

        # register
        executed = self.make_request(self.register_query("123"))
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])

    def test_register(self):
        """
        Register user, fail to register same user again
        """
        signal_received = False

        def receive_signal(sender, user, signal):
            self.assertTrue(user.id is not None)
            nonlocal signal_received
            signal_received = True

        user_registered.connect(receive_signal)

        # register
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.assertTrue(executed["token"])
        self.assertTrue(executed["refreshToken"])
        self.assertTrue(signal_received)

        # try to register again
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["username"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

        # try to register again
        executed = self.make_request(self.register_query(username="other_username"))
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["email"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    def test_register_duplicate_unique_email(self):

        user = self.register_user(
            email="foo@email.com",
            username="foo",
            verified=True,
            secondary_email="test@email.com",
        )

        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["email"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    def test_register_duplicate_unique_email_2(self):

        user = self.register_user(email="test@email.com", username="foo")

        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["email"])
        self.assertFalse(executed["token"])
        self.assertFalse(executed["refreshToken"])

    @mock.patch(
        "graphql_auth.models.UserStatus.send_activation_email",
        mock.MagicMock(side_effect=SMTPException),
    )
    def test_register_email_send_fail(self):
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.EMAIL_FAIL)
        self.assertEqual(len(get_user_model().objects.all()), 0)

    @mark.settings_b
    @skipif_django_21()
    def test_register_with_different_settings(self):
        """
        Register user, fail to register same user again
        """

        # register
        executed = self.make_request(self.register_query_b())
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)


class RegisterTestCase(RegisterTestCaseMixin, DefaultTestCase):
    def register_query(self, password="akssdgfbwkc", username="username"):
        return """
        mutation {
            register(
                email: "test@email.com",
                username: "%s",
                password1: "%s",
                password2: "%s"
            )
            { success, errors, token, refreshToken  }
        }
        """ % (
            username,
            password,
            password,
        )

    def register_query_b(self, password="akssdgfbwkc", username="username"):
        return """
        mutation {
            register(
                email: "test@email.com",
                username: "%s",
                password1: "%s",
                password2: "%s"
            )
            { success, errors  }
        }
        """ % (
            username,
            password,
            password,
        )

    def verify_query(self, token):
        return """
        mutation {
            verifyAccount(token: "%s")
                { success, errors }
            }
        """ % (
            token
        )


class RegisterRelayTestCase(RegisterTestCaseMixin, RelayTestCase):
    def register_query(self, password="akssdgfbwkc", username="username"):
        return """
        mutation {
         register(
         input:
            { email: "test@email.com", username: "%s", password1: "%s", password2: "%s" }
            )
            { success, errors, token, refreshToken  }
        }
        """ % (
            username,
            password,
            password,
        )

    def register_query_b(self, password="akssdgfbwkc", username="username"):
        return """
        mutation {
         register(
         input:
            { email: "test@email.com", username: "%s", password1: "%s", password2: "%s" }
            )
            { success, errors  }
        }
        """ % (
            username,
            password,
            password,
        )

    def verify_query(self, token):
        return """
        mutation {
        verifyAccount(input:{ token: "%s"})
            { success, errors  }
        }
        """ % (
            token
        )
