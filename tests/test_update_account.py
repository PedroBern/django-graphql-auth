from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class UpdateAccountTestCaseMixin:
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="foo@email.com", username="username", is_active=True,
        )
        self.user.set_password("sdfsdfff3f")
        self.user.save()

        self.user2 = get_user_model().objects.create(
            email="boo@email.com", username="username2", is_active=True,
        )
        self.user2.set_password("sdfsdfff3f")
        self.user2.save()

    def test_update_account_unauthenticated(self):
        executed = self.make_request(self.get_query())
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED,
        )

    def test_update_account_duplicate_field(self):
        variables = {"user": self.user}
        executed = self.make_request(self.get_query("username2"), variables)
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"])
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "username")

    def test_update_account(self):
        variables = {"user": self.user}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(
            executed["errors"], None,
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updated_username")


class UpdateAccountTestCase(UpdateAccountTestCaseMixin, DefaultTestCase):
    def get_query(self, username="updated_username"):
        return """
        mutation {
            updateAccount(username: "%s")
                { success, errors  }
        }
        """ % (
            username
        )


class UpdateAccountRelayTestCase(UpdateAccountTestCaseMixin, RelayTestCase):
    def get_query(self, username="updated_username"):
        return """
        mutation {
            updateAccount(input:{ username: "%s" })
                { success, errors }
        }
        """ % (
            username
        )
