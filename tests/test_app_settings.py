from graphql_auth import settings

from django.test import TestCase


class AppSettingsTestCase(TestCase):
    def test_reload_settings(self):
        self.assertTrue(settings.graphql_auth_settings.ALLOW_LOGIN_NOT_VERIFIED)
        user_settings = {"ALLOW_LOGIN_NOT_VERIFIED": False}
        settings.reload_graphql_auth_settings(
            setting="GRAPHQL_AUTH", value=user_settings
        )
        self.assertFalse(settings.graphql_auth_settings.ALLOW_LOGIN_NOT_VERIFIED)
