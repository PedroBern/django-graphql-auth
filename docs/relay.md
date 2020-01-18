# Relay

---

Simply import mutations from ``relay``:

```python

from graphql_auth import relay

class AuthMutation(graphene.ObjectType):
   register = relay.Register.Field()
```
