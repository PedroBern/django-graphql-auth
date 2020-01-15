from django.contrib.auth import get_user_model

from django.utils import timezone

from .testCases import RelayTestCase, DefaultTestCase
from graphql_auth.constants import Messages


class LoginTestCaseMixin:
    def setUp(self):
        self.archived_user = get_user_model().objects.create(
            email="foo@email.com",
            username="foo@email.com",
            is_active=False,
            last_login=timezone.now(),
        )
        self.archived_user.set_password("b23odxi2b34b")
        self.archived_user.save()

        self.not_verified_user = get_user_model().objects.create(
            email="baz@email.com", username="baz@email.com", is_active=False
        )
        self.not_verified_user.set_password("b23odxi2b34b")
        self.not_verified_user.save()

        self.verified_user = get_user_model().objects.create(
            email="gaa@email.com", username="gaa@email.com", is_active=True
        )
        self.verified_user.set_password("b23odxi2b34b")
        self.verified_user.save()

    def test_archived_user_becomes_active_on_login(self):
        """
        when archived user log in, becomes active again
        archived user is: is_active=False + last_login not None
        """
        self.assertEqual(self.archived_user.is_active, False)
        query = self.get_query(
            "email", self.archived_user.email, "b23odxi2b34b"
        )
        executed = self.make_request(query)
        self.archived_user.refresh_from_db()
        self.assertEqual(self.archived_user.is_active, True)
        self.assertTrue(executed["token"])

    def test_login_not_model_username_field(self):
        """
        try to login with different field
        graphql_jwt allow only with Model.USERNAME_FIELD
        """
        query = self.get_query(
            "username", self.verified_user.username, "b23odxi2b34b"
        )
        executed = self.make_request(query)
        self.assertTrue(executed["token"])

    def test_verified_user(self):
        query = self.get_query(
            "email", self.verified_user.email, "b23odxi2b34b"
        )
        executed = self.make_request(query)
        self.assertTrue(executed["token"])

    def test_not_verified_user_login(self):
        """
        not verified users can't log in
        """
        query = self.get_query(
            "email", self.not_verified_user.email, "b23odxi2b34b"
        )
        executed = self.make_request(query)
        self.assertFalse(executed["success"])
        self.assertTrue(executed["errors"]["nonFieldErrors"])


class LoginTestCase(LoginTestCaseMixin, DefaultTestCase):
    def get_query(self, field, username, password):
        return """
        mutation {
        tokenAuth(%s: "%s", password: "%s" )
            { token, success, errors  }
        }
        """ % (
            field,
            username,
            password,
        )


class LoginRelayTestCase(LoginTestCaseMixin, RelayTestCase):
    def get_query(self, field, username, password):
        return """
        mutation {
        tokenAuth(input:{ %s: "%s", password: "%s" })
            { token, success, errors  }
        }
        """ % (
            field,
            username,
            password,
        )
