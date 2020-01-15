from django.contrib.auth import get_user_model

from .utils import fake_email_templates
from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages
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

    @fake_email_templates
    def test_register(self):
        """
        Register user, fail to register same user again
        """

        # register
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

        # try to register again
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["username"])

    @fake_email_templates
    def test_register_with_email_verification(self):
        """
        register a user, check if is_active is False,
        get the activation token
        verify the account,
        try to verify again (already used token)
        try to verify with invalid token
        """

        # register
        executed = self.make_request(self.register_query())
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)

        # retrive
        user = get_user_model().objects.get(username="username")
        self.assertEqual(user.is_active, False)

        # activate
        token = get_token(user, "activation")
        payload = get_token_paylod(token, "activation")
        verify_query = self.verify_query(token)
        executed = self.make_request(verify_query)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        user.refresh_from_db()
        self.assertEqual(user.is_active, True)

        # try to activate again
        executed = self.make_request(verify_query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.ALREADY_VERIFIED,
        )

        # try to verify with fake token
        verify_query = self.verify_query("fake_token")
        executed = self.make_request(verify_query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.INVALID_TOKEN,
        )


class RegisterTestCase(RegisterTestCaseMixin, DefaultTestCase):
    def register_query(self, password="akssdgfbwkc"):
        return """
        mutation {
            register(
                email: "test@email.com",
                username: "username",
                password1: "%s",
                password2: "%s"
            )
            { success, errors  }
        }
        """ % (
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
    def register_query(self, password="akssdgfbwkc"):
        return """
        mutation {
         register(
         input:
            { email: "test@email.com", username: "username", password1: "%s", password2: "%s" }
            )
            { success, errors  }
        }
        """ % (
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
