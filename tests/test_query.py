from django.test import TestCase

from .testCases import DefaultTestCase


class QueryTestCase(DefaultTestCase):
    def setUp(self):
        self.user1 = self.register_user(
            email="foo@email.com", username="foo", verified=False
        )
        self.user2 = self.register_user(
            email="bar@email.com", username="bar", verified=True
        )
        self.user3 = self.register_user(
            email="gaa@email.com", username="gaa", verified=True, archived=True
        )

    def test_query(self):
        query = """
        query {
            users {
                edges {
                    node {
                        archived,
                        verified,
                        secondaryEmail
                    }
                }
            }
        }
        """
        executed = self.make_request(query)
        self.assertTrue(executed["edges"])
