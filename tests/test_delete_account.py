from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class DeleteAccountTestCaseMixin:
    def setUp(self):
        self.user1 = get_user_model().objects.create(
            email="foo@email.com", username="foo@email.com", is_active=True
        )
        self.user1.set_password("23kebsi23t4b")
        self.user1.save()
        self.user2 = get_user_model().objects.create(
            email="bar@email.com", username="bar@email.com", is_active=True
        )
        self.user2.set_password("23kebsi23t4b")
        self.user2.save()

    def test_not_authenticated(self):
        """
            try to delete not authenticated
        """
        query = self.make_query()
        executed = self.make_request(query)
        self.assertEqual(executed["success"], False)
        self.assertEqual(
            executed["errors"]["nonFieldErrors"], Messages.UNAUTHENTICATED,
        )

    def test_invalid_password(self):
        """
            try to delete account with invalid password
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
            try to delete account
        """
        query = self.make_query()
        variables = {"user": self.user1}
        executed = self.make_request(query, variables)
        self.assertEqual(executed["success"], True)
        self.assertEqual(executed["errors"], None)
        with self.assertRaises(ObjectDoesNotExist):
            self.user1.refresh_from_db()


class DeleteAccountTestCase(DeleteAccountTestCaseMixin, DefaultTestCase):
    def make_query(self, password="23kebsi23t4b"):
        return """
            mutation {
              deleteAccount(password: "%s") {
                success, errors
              }
            }
        """ % (
            password,
        )


class DeleteAccountRelayTestCase(DeleteAccountTestCaseMixin, RelayTestCase):
    def make_query(self, password="23kebsi23t4b"):
        return """
            mutation {
              deleteAccount(input: { password: "%s"}) {
                success, errors
              }
            }
        """ % (
            password,
        )
