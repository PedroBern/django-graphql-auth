from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase

from graphql_auth.constants import Messages
from graphql_auth.models import UserStatus


class ArchiveAccountTestCaseMixin:
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
        """
            try to archive account with invalid password
        """
        query = self.make_query(password="123")
        variables = {"user": self.user2}
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["password"], Messages.INVALID_PASSWORD)

    def test_valid_password(self):
        """
            try to archive account
        """
        query = self.make_query()
        variables = {"user": self.user2}
        self.assertEqual(self.user2.status.archived, False)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.status.archived, True)

    def test_revoke_refresh_tokens_on_archive_account(self):
        """
        when archive account, all refresh tokens should be revoked
        """

        executed = self.make_request(self.get_login_query())
        self.user2.refresh_from_db()
        refresh_tokens = self.user2.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertFalse(token.revoked)

        query = self.make_query()
        variables = {"user": self.user2}
        self.assertEqual(self.user2.status.archived, False)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.status.archived, True)

        self.user2.refresh_from_db()
        refresh_tokens = self.user2.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertTrue(token.revoked)

    def test_not_verified_user(self):
        """
            try to archive account
        """
        query = self.make_query()
        variables = {"user": self.user1}
        self.assertEqual(self.user1.status.archived, False)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.NOT_VERIFIED)
        self.assertEqual(self.user1.status.archived, False)


class ArchiveAccountTestCase(ArchiveAccountTestCaseMixin, DefaultTestCase):
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
              archiveAccount(password: "%s") {
                success, errors
              }
            }
        """ % (
            password or self.default_password,
        )


class ArchiveAccountRelayTestCase(ArchiveAccountTestCaseMixin, RelayTestCase):
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
              archiveAccount(input: { password: "%s"}) {
                success, errors
              }
            }
        """ % (
            password or self.default_password,
        )
