import pprint
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from graphene.test import Client
from graphene.types.schema import Schema

from graphql_auth.models import UserStatus

from .schema import default_schema, relay_schema


class TestBase(TestCase):
    """
    provide make_request helper to easily make
    requests with context variables.

    Return a shortcut of the client.execute["data"]["<query name>"].

    example:
        query = `
            mutation {
             register ...
            }
        `
        return client.execute["data"]["register"]
    """

    default_password = "23kegbsi7g2k"

    def register_user(
        self,
        password=None,
        verified=False,
        archived=False,
        secondary_email="",
        *args,
        **kwargs
    ):
        if kwargs.get("username"):
            kwargs.update({"first_name": kwargs.get("username")})
        user = get_user_model().objects.create(*args, **kwargs)
        user.set_password(password or self.default_password)
        user.save()
        user_status = UserStatus._default_manager.get(user=user)
        user_status.verified = verified
        user_status.archived = archived
        user_status.secondary_email = secondary_email
        user_status.save()
        user_status.refresh_from_db()
        user.refresh_from_db()
        return user

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
        finally:
            pprint.pprint(executed)


class RelayTestCase(TestBase):
    def make_request(self, *args, **kwargs):
        client = Client(relay_schema)
        return super().make_request(client=client, *args, **kwargs)


class DefaultTestCase(TestBase):
    def make_request(self, *args, **kwargs):
        client = Client(default_schema)
        return super().make_request(client=client, *args, **kwargs)
