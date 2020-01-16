from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class ArchiveAccountTestCaseMixin:
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            email="foo@email.com", username="foo@email.com", is_active=True
        )
        self.user1.set_password("23kegbsi7g2k")
        self.user1.save()
        self.user2 = get_user_model().objects.create(
            email="bar@email.com", username="bar@email.com", is_active=True
        )
        self.user2.set_password("23kegbsi7g2k")
        self.user2.save()

    def test_not_authenticated(self):
        """
            try to archive not authenticated
        """
        query = self.make_query()
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED,
        )

    def test_invalid_password(self):
        """
            try to archive account with invalid password
        """
        query = self.make_query(password="123")
        variables = {"user": self.user1}
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["password"], Messages.INVALID_PASSWORD,
        )

    def test_valid_password(self):
        """
            try to archive account
        """
        query = self.make_query()
        variables = {"user": self.user1}
        self.assertEqual(self.user1.is_active, True)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.assertEqual(self.user1.is_active, False)

    def test_revoke_refresh_tokens_on_archive_account(self):
        """
        when archive account, all refresh tokens should be revoked
        """

        executed = self.make_request(self.get_login_query())
        self.user1.refresh_from_db()
        refresh_tokens = self.user1.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertFalse(token.revoked)

        query = self.make_query()
        variables = {"user": self.user1}
        self.assertEqual(self.user1.is_active, True)
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.assertEqual(self.user1.is_active, False)

        self.user1.refresh_from_db()
        refresh_tokens = self.user1.refresh_tokens.all()
        for token in refresh_tokens:
            self.assertTrue(token.revoked)


class ArchiveAccountTestCase(ArchiveAccountTestCaseMixin, DefaultTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                email: "foo@email.com",
                password: "23kegbsi7g2k",
            )
            { success, errors, refreshToken }
        }
        """

    def make_query(self, password="23kegbsi7g2k"):
        return """
            mutation {
              archiveAccount(password: "%s") {
                success, errors
              }
            }
        """ % (
            password,
        )


class ArchiveAccountRelayTestCase(ArchiveAccountTestCaseMixin, RelayTestCase):
    def get_login_query(self):
        return """
        mutation {
            tokenAuth(
                input: {
                    email: "foo@email.com",
                    password: "23kegbsi7g2k",
                }
            )
            { success, errors, refreshToken }
        }
        """

    def make_query(self, password="23kegbsi7g2k"):
        return """
            mutation {
              archiveAccount(input: { password: "%s"}) {
                success, errors
              }
            }
        """ % (
            password,
        )
