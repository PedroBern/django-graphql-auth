from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class UpdateAccountTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="foo@email.com", username="foo", verified=False
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True
        )

    def test_update_account_unauthenticated(self):
        executed = self.make_request(self.get_query())
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED,
        )

    def test_update_account_not_verified(self):
        variables = {"user": self.user1}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.NOT_VERIFIED,
        )

    def test_update_account(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(
            executed["errors"], None,
        )
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, "firstname")

    def test_invalid_form(self):
        variables = {"user": self.user2}
        executed = self.make_request(
            self.get_query("longstringwithmorethan30characters"), variables
        )
        self.assertEqual(executed["success"], False)
        self.assertTrue(executed["errors"]["firstName"])
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, "")


class UpdateAccountTestCase(UpdateAccountTestCaseMixin, DefaultTestCase):
    def get_query(self, first_name="firstname"):
        return """
        mutation {
            updateAccount(firstName: "%s")
                { success, errors  }
        }
        """ % (
            first_name
        )


class UpdateAccountRelayTestCase(UpdateAccountTestCaseMixin, RelayTestCase):
    def get_query(self, first_name="firstname"):
        return """
        mutation {
            updateAccount(input:{ firstName: "%s" })
                { success, errors }
        }
        """ % (
            first_name
        )
