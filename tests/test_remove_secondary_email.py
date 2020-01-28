from django.contrib.auth import get_user_model

from graphql_auth.constants import Messages


from .testCases import RelayTestCase, DefaultTestCase


class RemoveSecondaryEmailCaseMixin:
    def setUp(self):
        self.user = self.register_user(
            email="bar@email.com",
            username="bar",
            verified=True,
            secondary_email="secondary@email.com",
        )

    def test_remove_email(self):
        executed = self.make_request(self.query(), {"user": self.user})
        self.assertEqual(executed["success"], True)
        self.assertFalse(executed["errors"])
        self.user.refresh_from_db()
        self.assertEqual(self.user.status.secondary_email, None)


class RemoveSecondaryEmailCase(RemoveSecondaryEmailCaseMixin, DefaultTestCase):
    def query(self, password=None):
        return """
        mutation {
            removeSecondaryEmail(password: "%s")
                { success, errors }
            }
        """ % (
            password or self.default_password
        )


class RemoveSecondaryEmailRelayTestCase(RemoveSecondaryEmailCaseMixin, RelayTestCase):
    def query(self, password=None):
        return """
        mutation {
        removeSecondaryEmail(input:{ password: "%s"})
            { success, errors  }
        }
        """ % (
            password or self.default_password
        )
