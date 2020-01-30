# Relay

---

Import mutations from the ``relay`` module:

```python

from graphql_auth import relay

class AuthMutation(graphene.ObjectType):
   register = relay.Register.Field()
```
