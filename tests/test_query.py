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
                        secondaryEmail,
                        pk
                    }
                }
            }
        }
        """
        executed = self.make_request(query)
        self.assertTrue(executed["edges"])

    def test_db_queries(self):
        """
        Querying users should only use 2 db queries.

        1. SELECT COUNT(*) AS "__count" FROM "auth_user"
        2. SELECT ... FROM "auth_user"
            LEFT OUTER JOIN "graphql_auth_userstatus" ON (
                "auth_user"."id" = "graphql_auth_userstatus"."user_id"
            )
            LIMIT 3
        """

        query = """
        query {
            users {
                edges {
                    node {
                        archived,
                        verified,
                        secondaryEmail,
                        pk
                    }
                }
            }
        }
        """
        with self.assertNumQueries(2):
            executed = self.make_request(query)
        self.assertTrue(executed["edges"])

    def test_me_authenticated(self):
        query = """
        query {
            me {
                username
            }
        }
        """
        executed = self.make_request(query, variables={"user": self.user2})
        self.assertTrue(executed["username"])

    def test_me_anonymous(self):
        query = """
        query {
            me {
                username
            }
        }
        """
        executed = self.make_request(query)
        self.assertIsNone(executed)

    def test_public_user_query(self):
        query = """
        query {
            publicUser {
                verified
            }
        }
        """
        executed = self.make_request(query, variables={"user": self.user1})
        self.assertEqual(executed, {"verified": False})
