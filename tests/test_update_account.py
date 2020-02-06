from pytest import mark
from django.contrib.auth import get_user_model

from .testCases import RelayTestCase, DefaultTestCase
from .decorators import skipif_django_21

from graphql_auth.constants import Messages


class UpdateAccountTestCaseMixin:
    def setUp(self):
        self.user1 = self.register_user(
            email="foo@email.com", username="foo", verified=False, first_name="foo"
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True, first_name="bar"
        )
        self.user3 = self.register_user(
            email="gaa@email.com", username="gaa", verified=True, first_name="gaa"
        )

    def test_update_account_unauthenticated(self):
        executed = self.make_request(self.get_query())
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED)

    def test_update_account_not_verified(self):
        variables = {"user": self.user1}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], False)
        self.assertEqual(executed["errors"]["nonFieldErrors"], Messages.NOT_VERIFIED)

    def test_update_account(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
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
        self.assertEqual(self.user2.first_name, "bar")

    @mark.settings_b
    @skipif_django_21()
    def test_update_account_list_on_settings(self):
        variables = {"user": self.user2}
        executed = self.make_request(self.get_query(), variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, "firstname")

    @mark.settings_b
    @skipif_django_21()
    def test_update_account_non_field_errors(self):
        """
        on settings b: first and last name are unique together,
        so we can test the non field error for the error type
        """
        # first update a user
        mutation = self.get_unique_together_test_query()

        variables = {"user": self.user2}
        executed = self.make_request(mutation, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        self.user2.refresh_from_db()
        self.assertEqual(self.user2.first_name, "first")

        # then try to update other user with same mutation
        variables = {"user": self.user3}
        executed = self.make_request(mutation, variables)
        self.assertEqual(executed["success"], False)
        print(executed)
        self.assertTrue(executed["errors"]["nonFieldErrors"])


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

    def get_unique_together_test_query(self):
        return """
        mutation {
            updateAccount(firstName: "first", lastName: "last")
                { success, errors  }
        }
        """


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

    def get_unique_together_test_query(self):
        return """
        mutation {
            updateAccount(input: {firstName: "first", lastName: "last"})
                { success, errors  }
        }
        """
