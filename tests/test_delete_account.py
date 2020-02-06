import django
from pytest import mark

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .testCases import RelayTestCase, DefaultTestCase
from .decorators import skipif_django_21

from graphql_auth.constants import Messages
from graphql_auth.models import UserStatus


class DeleteAccountTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(email="foo@email.com", username="foo")
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True
        )

    def test_not_authenticated(self):
        """
            try to archive not authenticated
        """
        query = self.make_query()
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED)

    def test_invalid_password(self):
        query = self.make_query(password="123")
        variables = {"user": self.user2}
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["password"], Messages.INVALID_PASSWORD)

    def test_revoke_refresh_tokens_on_delete_account(self):

        executed = self.make_request(self.get_login_query())
        self.user2.refresh_from_db()
        refresh_tokens = self.user2.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertFalse(token.revoked)

        query = self.make_query()
        variables = {"user": self.user2}
        self.assertEqual(self.user2.is_active, True)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.is_active, False)

        self.user2.refresh_from_db()
        refresh_tokens = self.user2.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertTrue(token.revoked)

    def test_not_verified_user(self):
        query = self.make_query()
        variables = {"user": self.user1}
        self.assertEqual(self.user1.is_active, True)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.NOT_VERIFIED)
        self.assertEqual(self.user1.is_active, True)

    def test_valid_password(self):
        query = self.make_query()
        variables = {"user": self.user2}
        self.assertEqual(self.user2.is_active, True)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.is_active, False)

    @mark.settings_b
    @skipif_django_21()
    def test_valid_password_permanently_delete(self):
        query = self.make_query()
        variables = {"user": self.user2}
        self.assertEqual(self.user2.is_active, True)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        with self.assertRaises(ObjectDoesNotExist):
            self.user2.refresh_from_db()

    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                email: "foo@email.com",
                password: "%s",
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def make_query(self, password=None):
        return """
            mutation {
              deleteAccount(password: "%s") {
                success, errors
              }
            }
        """ % (
            password or self.default_password,
        )


class DeleteAccountTestCase(DeleteAccountTestCaseMixin, DefaultTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                email: "foo@email.com",
                password: "%s",
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def make_query(self, password=None):
        return """
            mutation {
              deleteAccount(password: "%s") {
                success, errors
              }
            }
        """ % (
            password or self.default_password,
        )


class DeleteAccountRelayTestCase(DeleteAccountTestCaseMixin, RelayTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                input: {
                    email: "foo@email.com",
                    password: "%s",
                }
            )
            { success, errors, refreshToken }
        }
        """ % (
            self.default_password,
        )

    def make_query(self, password=None):
        return """
            mutation {
              deleteAccount(input: { password: "%s"}) {
                success, errors
              }
            }
        """ % (
            password or self.default_password,
        )
