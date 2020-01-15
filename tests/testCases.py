import re

from graphene.test import Client
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from .schema import relay_schema, default_schema


from graphene.types.schema import Schema


class TestBase(TestCase):
    """
    provide make_request helper to easily make a WSGIRequest
    with context variables.
    Return a shortcut of the client.execute["data"]["query name"].

    example:
        query = `
            mutation {
             register ...
            }
        `
        return client.execute["data"]["register"]
    """

    def make_request(
        self, query, variables={"user": AnonymousUser()}, raw=False, client=None
    ):
        request_factory = RequestFactory()
        my_request = request_factory.post("/graphql/")

        for key in variables:
            setattr(my_request, key, variables[key])

        executed = client.execute(query, context=my_request)
        if raw:
            return executed
        pattern = r"{\s*(?P<target>\w*)"
        m = re.search(pattern, query)
        m = m.groupdict()
        try:
            return executed["data"][m["target"]]
        except:
            print("\nInvalid query!")
            raise Exception(executed["errors"])


class RelayTestCase(TestBase):
    def make_request(self, *args, **kwargs):
        client = Client(relay_schema)
        return super().make_request(client=client, *args, **kwargs)


class DefaultTestCase(TestBase):
    def make_request(self, *args, **kwargs):
        client = Client(default_schema)
        return super().make_request(client=client, *args, **kwargs)
