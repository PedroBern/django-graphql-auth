# API

---

## Query

GraphQL Auth provides the UserQuery to query users with some useful filters.

GraphQL Auth also provides the MeQuery to retrieve data for the currently authenticated user.

### UserQuery

```
from graphql_auth.schema import UserQuery
```

The easiest way to explore it is by using [graphiQL](https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/#creating-graphql-and-graphiql-views).

Examples from the [quickstart](quickstart.md):

```tab="query1"
query {
  users {
    edges {
      node {
        username,
        archived,
        verified,
        email,
        secondaryEmail,
      }
    }
  }
}
```

```tab="response1"
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "username": "user1",
            "archived": false,
            "verified": false,
            "email": "user1@email.com",
            "secondaryEmail": null
          }
        },
        {
          "node": {
            "username": "user2",
            "archived": false,
            "verified": true,
            "email": "user2@email.com",
            "secondaryEmail": null
          }
        },
        {
          "node": {
            "username": "user3",
            "archived": true,
            "verified": true,
            "email": "user3@email.com",
            "secondaryEmail": null
          }
        },
        {
          "node": {
            "username": "user4",
            "archived": false,
            "verified": true,
            "email": "user4@email.com",
            "secondaryEmail": "user4_secondary@email.com"
          }
        }
      ]
    }
  }
}
```

```tab="query2"
query {
  users (last: 1){
    edges {
      node {
        id,
        username,
        email,
        isActive,
        archived,
        verified,
        secondaryEmail
      }
    }
  }
}
```

```tab="response2"
{
  "data": {
    "users": {
      "edges": [
        {
          "node": {
            "id": "VXNlck5vZGU6NQ==",
            "username": "new_user",
            "email": "new_user@email.com",
            "isActive": true,
            "archived": false,
            "verified": false,
            "secondaryEmail": null
          }
        }
      ]
    }
  }
}
```

```tab="query3"
query {
  user (id: "VXNlck5vZGU6NQ=="){
    username,
    verified
  }
}
```

```tab="response3"
{
  "data": {
    "user": {
      "username": "new_user",
      "verified": true
    }
  }
}
```

### MeQuery

```
from graphql_auth.schema import MeQuery
```

Since this query requires an authenticated user it can be explored by using the [insomnia API client](https://insomnia.rest/). See the [quickstart](quickstart.md) for more on how to use Insomnia.

Example from the [quickstart](quickstart.md):

```tab="query"
query {
  me {
    username,
    verified
  }
}
```

```tab="response"
{
  "data": {
    "user": {
      "username": "new_user",
      "verified": true
    }
  }
}
```

---

## Mutations

All mutations can be imported like this:

```python tab="mutations"
from graphql_auth import mutations

# on your mutations
register = mutations.Register
```

```python tab="relay"
from graphql_auth import relay

# on your mutations
register = use relay.Register
```

### Standard response

All mutations return a standard response containing `#!python errors` and `#!python success`.

- Example:

```python tab="graphql"
mutation {
  register(
    email: "new_user@email.com",
    username: "new_user",
    password1: "123456",
    password2: "123456",
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

```python tab="response"
{
  "data": {
    "register": {
      "success": false,
      "errors": {
        "password2": [
          {
            "message": "This password is too short. It must contain at least 8 characters.",
            "code": "password_too_short"
          },
          {
            "message": "This password is too common.",
            "code": "password_too_common"
          },
          {
            "message": "This password is entirely numeric.",
            "code": "password_entirely_numeric"
          }
        ]
      },
      "token": null
      "refreshToken": null
    }
  }
}
```

```python tab="relay" hl_lines="3 8"
mutation {
  register(
    input: {
      email: "new_user@email.com",
      username: "new_user",
      password1: "123456",
      password2: "123456",
    }
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

---

### Public

Public mutations don't require user to be logged in. You should add all of them in `#!python GRAPHQL_JWT["JWT_ALLOW_ANY_CLASSES"]` setting.

---

#### ObtainJSONWebToken

{{ api.ObtainJSONWebToken }}

```bash tab="graphql"
mutation {
  tokenAuth(
    # username or email
    email: "skywalker@email.com"
    password: "123456super"
  ) {
    success,
    errors,
    token,
    refreshToken,
    unarchiving,
    user {
      id,
      username
    }
  }
}
```

```bash tab="success"
{
  "data": {
    "tokenAuth": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImV4cCI6MTU3OTQ1ODI2Niwib3JpZ0lhdCI6MTU3OTQ1Nzk2Nn0.BKz4ohxQCGtJWnyd5tIbYFD2kpGYDiAVzWTDO2ZyUYY",
      "refreshToken": "5f5fad67cd043437952ddde2750be20201f1017b",
      "unarchiving": false,
      "user": {
        "id": "VXNlck5vZGU6MQ==",
        "username": "skywalker"
      }
    }
  }
}
```

```bash tab="relay"
mutation {
  tokenAuth(
    input: {
      email: "skywalker@email.com"
      password: "123456super"
    }
  ) {
    success,
    errors,
    token,
    refreshToken,
    user {
      id,
      username
    }
  }
}
```

```bash tab="Invalid credentials"
{
  "data": {
    "tokenAuth": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Please, enter valid credentials.",
            "code": "invalid_credentials"
          }
        ]
      },
      "token": null,
      "refreshToken": null,
      "unarchiving": false,
      "user": null
    }
  }
}
```

---
#### PasswordSet

{{ api.PasswordSet }}

```bash tab="graphql"
mutation {
  passwordSet(
    token: "1eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6InBhc3N3b3JkX3Jlc2V0In0:1itExL:op0roJi-ZbO9cszNEQMs5mX3c6s",
    newPassword1: "supersecretpassword",
    newPassword2: "supersecretpassword"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "passwordSet": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  passwordSet(
    input: {
      token: "1eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6InBhc3N3b3JkX3Jlc2V0In0:1itExL:op0roJi-ZbO9cszNEQMs5mX3c6s",
      newPassword1: "supersecretpassword",
      newPassword2: "supersecretpassword"
    }
  ) {
    success,
    errors
  }
}
```

```bash tab="Invalid token"
{
  "data": {
    "passwordSet": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      }
    }
  }
}
```

```bash tab="Password mismatch"
{
  "data": {
    "passwordSet": {
      "success": false,
      "errors": {
        "newPassword2": [
          {
            "message": "The two password fields didn’t match.",
            "code": "password_mismatch"
          }
        ]
      }
    }
  }
}
```

```bash tab="Password validators"
{
  "data": {
    "passwordSet": {
      "success": false,
      "errors": {
        "newPassword2": [
          {
            "message": "This password is too short. It must contain at least 8 characters.",
            "code": "password_too_short"
          },
          {
            "message": "This password is too common.",
            "code": "password_too_common"
          },
          {
            "message": "This password is entirely numeric.",
            "code": "password_entirely_numeric"
          }
        ]
      }
    }
  }
}
```

```bash tab="Password Set"
{
  "data": {
    "passwordSet": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Password already set for account.",
            "code": "password_already_set"
          }
        ]
      }
    }
  }
}
```

---

#### PasswordReset

{{ api.PasswordReset }}

```bash tab="graphql"
mutation {
  passwordReset(
    token: "1eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6InBhc3N3b3JkX3Jlc2V0In0:1itExL:op0roJi-ZbO9cszNEQMs5mX3c6s",
    newPassword1: "supersecretpassword",
    newPassword2: "supersecretpassword"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "passwordReset": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  passwordReset(
    input: {
      token: "1eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6InBhc3N3b3JkX3Jlc2V0In0:1itExL:op0roJi-ZbO9cszNEQMs5mX3c6s",
      newPassword1: "supersecretpassword",
      newPassword2: "supersecretpassword"
    }
  ) {
    success,
    errors
  }
}
```

```bash tab="Invalid token"
{
  "data": {
    "passwordReset": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      }
    }
  }
}
```

```bash tab="Password mismatch"
{
  "data": {
    "passwordReset": {
      "success": false,
      "errors": {
        "newPassword2": [
          {
            "message": "The two password fields didn’t match.",
            "code": "password_mismatch"
          }
        ]
      }
    }
  }
}
```

```bash tab="Password validators"
{
  "data": {
    "passwordReset": {
      "success": false,
      "errors": {
        "newPassword2": [
          {
            "message": "This password is too short. It must contain at least 8 characters.",
            "code": "password_too_short"
          },
          {
            "message": "This password is too common.",
            "code": "password_too_common"
          },
          {
            "message": "This password is entirely numeric.",
            "code": "password_entirely_numeric"
          }
        ]
      }
    }
  }
}
```

---

#### RefreshToken

{{ api.VerifyOrRefreshOrRevokeToken }}


```bash tab="graphql"
mutation {
  refreshToken(
    refreshToken: "d9b58dce41cf14549030873e3fab3be864f76ce44"
  ) {
    success,
    errors,
    payload,
    refreshExpiresIn,
    token,
    refreshToken
  }
}
```

```bash tab="success"
{
  "data": {
    "refreshToken": {
      "success": true,
      "errors": null,
      "payload": {
        "username": "skywalker",
        "exp": 1601646082,
        "origIat": 1601645782
      },
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImV4cCI6MTYwMTY0NjA4Miwib3JpZ0lhdCI6MTYwMTY0NTc4Mn0.H6gLeky7lX834kBI5RFT8ziNNfGOL3XXg1dRwvpQuRI",
      "refreshToken": "a64f732b4e00432f2ff1b47537a11458be13fc82",
      "refreshExpiresIn": 1602250582
    }
  }
}
```

```bash tab="relay"
mutation {
  refreshToken(
    input: {
      refreshToken: "d9b58dce41cf14549030873e3fab3be864f76ce44"
    }
  ) {
    success,
    errors,
    payload,
    refreshExpiresIn,
    token,
    refreshToken
  }
}
```


```bash tab="Invalid token"
{
  "data": {
    "refreshToken": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      }
    }
  }
}
```


---

#### Register

{{ api.Register }}


```bash tab="graphql"
mutation {
  register(
    email:"skywalker@email.com",
    username:"skywalker",
    password1: "qlr4nq3f3",
    password2:"qlr4nq3f3"
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

```bash tab="success"
{
  "data": {
    "register": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvZWpvZSIsImV4cCI6MTU4MDE0MjE0MCwib3JpZ0lhdCI6MTU4MDE0MTg0MH0.BGUSGKUUd7IuHnWKy8V6MU3slJ-DHsyAdAjGrGb_9fw",
      "refreshToken": "d9b58dce41cf14549030873e3fab3be864f76ce44"
    }
  }
}
```

```bash tab="relay"
mutation {
  register(
    input: {
      email:"skywalker@email.com",
      username:"skywalker",
      password1: "qlr4nq3f3",
      password2:"qlr4nq3f3"
    }
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```


```bash tab="unique"
{
  "data": {
    "register": {
      "success": false,
      "errors": {
        "username": [
          {
            "message": "A user with that username already exists.",
            "code": "unique"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="password mismatch"
{
  "data": {
    "register": {
      "success": false,
      "errors": {
        "password2": [
          {
            "message": "The two password fields didn’t match.",
            "code": "password_mismatch"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="password validators"
{
  "data": {
    "register": {
      "success": false,
      "errors": {
        "password2": [
          {
            "message": "This password is too short. It must contain at least 8 characters.",
            "code": "password_too_short"
          },
          {
            "message": "This password is too common.",
            "code": "password_too_common"
          },
          {
            "message": "This password is entirely numeric.",
            "code": "password_entirely_numeric"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="invalid email"
{
  "data": {
    "register": {
      "success": false,
      "errors": {
        "email": [
          {
            "message": "Enter a valid email address.",
            "code": "invalid"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

---

#### ResendActivationEmail

{{ api.ResendActivationEmail }}


```bash tab="graphql"
mutation {
  resendActivationEmail(
    email:"skywalker@email.com",
  ) {
    success,
    errors

  }
}
```

```bash tab="success"
{
  "data": {
    "register": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  resendActivationEmail(
    input: {
      email:"skywalker@email.com",
    }
  ) {
    success,
    errors

  }
}
```


```bash tab="Already verified"
{
  "data": {
    "resendActivationEmail": {
      "success": false,
      "errors": {
        "email": [
          [
            {
              "message": "Account already verified.",
              "code": "already_verified"
            }
          ]
        ]
      }
    }
  }
}
```

```bash tab="Invalid email"
{
  "data": {
    "resendActivationEmail": {
      "success": false,
      "errors": {
        "email": [
          {
            "message": "Enter a valid email address.",
            "code": "invalid"
          }
        ]
      }
    }
  }
}
```

```bash tab="Email fail"
{
  "data": {
    "resendActivationEmail": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
            {
              "message": "Failed to send email.",
              "code": "email_fail"
            }
        ]
      }
    }
  }
}
```

---

#### RevokeToken

{{ api.VerifyOrRefreshOrRevokeToken }}


```bash tab="graphql"
mutation {
  revokeToken(
    refreshToken: "a64f732b4e00432f2ff1b47537a11458be13fc82"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "revokeToken": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  revokeToken(
    input: {
      refreshToken: "a64f732b4e00432f2ff1b47537a11458be13fc82"
    }
  ) {
    success,
    errors
  }
}
```


```bash tab="Invalid token"
{
  "data": {
    "revokeToken": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      }
    }
  }
}
```

---

#### SendPasswordResetEmail

{{ api.SendPasswordResetEmail }}


```bash tab="graphql"
mutation {
  sendPasswordResetEmail(
    email: "skywalker@email.com"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "register": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  sendPasswordResetEmail(
    input: {
      email: "skywalker@email.com"
    }
  ) {
    success,
    errors
  }
}
```


```bash tab="Invalid email"
{
  "data": {
    "sendPasswordResetEmail": {
      "success": false,
      "errors": {
        "email": [
          {
            "message": "Enter a valid email address.",
            "code": "invalid"
          }
        ]
      }
    }
  }
}
```

```bash tab="Email fail"
{
  "data": {
    "sendPasswordResetEmail": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
            {
              "message": "Failed to send email.",
              "code": "email_fail"
            }
        ]
      }
    }
  }
}
```

```bash tab="Email not verified"
{
  "data": {
    "sendPasswordResetEmail": {
      "success": false,
      "errors": {
        "email": [
          {
            "message": "Verify your account. A new verification email was sent.",
            "code": "not_verified"
          }
        ]
      }
    }
  }
}
```

---

#### VerifyAccount

{{ api.VerifyAccount }}


```bash tab="graphql"
mutation {
  verifyAccount(
    token:"eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6ImFjdGl2YXRpb24ifQ:1itC5A:vJhRJwBcrNxvmEKxHrZa6Yoqw5Q",
  ) {
    success, errors
  }
}
```

```bash tab="success"
{
  "data": {
    "verifyAccount": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  verifyAccount(
    input: {
      token:"eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6ImFjdGl2YXRpb24ifQ:1itC5A:vJhRJwBcrNxvmEKxHrZa6Yoqw5Q",
    }
  ) {
    success, errors
  }
}
```


```bash tab="Invalid token"
{
  "data": {
    "verifyAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      }
    }
  }
}
```

```bash tab="Already verified"
{
  "data": {
    "verifyAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Account already verified.",
            "code": "already_verified"
          }
        ]
      }
    }
  }
}
```

---

#### VerifySecondaryEmail

{{ api.VerifySecondaryEmail }}

```bash tab="graphql"
mutation {
  verifySecondaryEmail(
    token: "eyJ1c2VybmFtZSI6Im5ld191c2VyMSIsImFjdGlvbiI6ImFjdGl2YXRpb25fc2Vjb25kYXJ5X2VtYWlsIiwic2Vjb25kYXJ5X2VtYWlsIjoibXlfc2Vjb25kYXJ5X2VtYWlsQGVtYWlsLmNvbSJ9:1ivhfJ:CYZswRKV3avWA8cb41KqZ1-zdVo"
    ) {
    success, errors
  }
}
```

```bash tab="success"
{
  "data": {
    "verifySecondaryEmail": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  verifySecondaryEmail(
    input: {
      token: "eyJ1c2VybmFtZSI6Im5ld191c2VyMSIsImFjdGlvbiI6ImFjdGl2YXRpb25fc2Vjb25kYXJ5X2VtYWlsIiwic2Vjb25kYXJ5X2VtYWlsIjoibXlfc2Vjb25kYXJ5X2VtYWlsQGVtYWlsLmNvbSJ9:1ivhfJ:CYZswRKV3avWA8cb41KqZ1-zdVo"
    }
  ) {
    success, errors
  }
}
```

```bash tab="Invalid token"
{
  "data": {
    "verifySecondaryEmail": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      }
    }
  }
}
```

```bash tab="Expired token"
{
  "data": {
    "verifySecondaryEmail": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Expired token.",
            "code": "expired_token"
          }
        ]
      }
    }
  }
}
```


---

#### VerifyToken

{{ api.VerifyOrRefreshOrRevokeToken }}


```bash tab="graphql"
mutation {
  verifyToken(
    token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImV4cCI6MTU3OTQ1ODY3Miwib3JpZ0lhdCI6MTU3OTQ1ODM3Mn0.rrB4sMA-v7asrr8Z2ru69U1x-d98DuEJVBnG2F1C1S0"
  ) {
    success,
    errors,
    payload
  }
}
```

```bash tab="success"
{
  "data": {
    "verifyToken": {
      "success": true,
      "errors": null,
      "payload": {
        "username": "skywalker",
        "exp": 1579458672,
        "origIat": 1579458372
      }
    }
  }
}
```

```bash tab="relay"
mutation {
  verifyToken(
    input:
      token: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImV4cCI6MTU3OTQ1ODY3Miwib3JpZ0lhdCI6MTU3OTQ1ODM3Mn0.rrB4sMA-v7asrr8Z2ru69U1x-d98DuEJVBnG2F1C1S0"
    }
  ) {
    success,
    errors,
    payload
  }
}
```


```bash tab="Invalid token"
{
  "data": {
    "verifyToken": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid token.",
            "code": "invalid_token"
          }
        ]
      },
      "payload": null
    }
  }
}
```

```bash tab="Expired token"
{
  "data": {
    "verifyToken": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Expired token.",
            "code": "expired_token"
          }
        ]
      }
    }
  }
}
```

---

### Protected

Protected mutations require the http Authorization header.

If you send a request **without** the http Authorization header, or a **bad token**:

- If using `graphql_jwt.backends.JSONWebTokenBackend`, it will raise.
- If using `graphql_auth.backends.GraphQLAuthBackend`, it will return a standard response, with `success=False` and `errors`.

As explained on the [installation guide](installation.md)

---

#### ArchiveAccount

{{ api.ArchiveAccount }}


```bash tab="graphql"
mutation {
  archiveAccount(
    password: "supersecretpassword",
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "register": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  archiveAccount(
    input: {
      password: "supersecretpassword",
    }
  ) {
    success,
    errors
  }
}
```


```bash tab="Unauthenticated"
{
  "data": {
    "archiveAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Unauthenticated.",
            "code": "unauthenticated"
          }
        ]
      }
    }
  }
}
```

```bash tab="Invalid password"
{
  "data": {
    "archiveAccount": {
      "success": false,
      "errors": {
        "password": [
          {
            "message": "Invalid password.",
            "code": "invalid_password"
          }
        ]
      }
    }
  }
}
```

```bash tab="Not verified"
{
  "data": {
    "archiveAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Please verify your account."
            "code": "not_verified"
          }
        ]
      }
    }
  }
}
```

---

#### DeleteAccount

{{ api.DeleteAccount }}


```bash tab="graphql"
mutation {
  deleteAccount(
    password: "supersecretpassword",
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "deleteAccount": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  deleteAccount(
    input: {
      password: "supersecretpassword",
    }
  ) {
    success,
    errors
  }
}
```


```bash tab="Unauthenticated"
{
  "data": {
    "deleteAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Unauthenticated.",
            "code": "unauthenticated"
          }
        ]
      }
    }
  }
}
```

```bash tab="Invalid password"
{
  "data": {
    "deleteAccount": {
      "success": false,
      "errors": {
        "password": [
          {
            "message": "Invalid password.",
            "code": "invalid_password"
          }
        ]
      }
    }
  }
}
```

```bash tab="Not verified"
{
  "data": {
    "deleteAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Please verify your account."
            "code": "not_verified"
          }
        ]
      }
    }
  }
}
```

---

#### PasswordChange

{{ api.PasswordChange }}

```bash tab="graphql"
mutation {
 passwordChange(
    oldPassword: "supersecretpassword",
    newPassword1: "123456super",
     newPassword2: "123456super"
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```

```bash tab="success"
{
  "data": {
    "passwordChange": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImpvZWpvZSIsImV4cCI6MTU4MDE0MjE0MCwib3JpZ0lhdCI6MTU4MDE0MTg0MH0.BGUSGKUUd7IuHnWKy8V6MU3slJ-DHsyAdAjGrGb_9fw",
      "refreshToken": "67eb63ba9d279876d3e9ae4d39c311e845e728fc"
    }
  }
}
```

```bash tab="relay"
mutation {
 passwordChange(
   input: {
      oldPassword: "supersecretpassword",
      newPassword1: "123456super",
       newPassword2: "123456super"
    }
  ) {
    success,
    errors,
    token,
    refreshToken
  }
}
```


```bash tab="Unauthenticated"
{
  "data": {
    "passwordChange": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Unauthenticated.",
            "code": "unauthenticated"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="Not verified"
{
  "data": {
    "passwordChange": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Please verify your account."
            "code": "not_verified"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="Password validation"
{
  "data": {
    "passwordChange": {
      "success": false,
      "errors": {
        "newPassword2": [
          {
            "message": "This password is too short. It must contain at least 8 characters.",
            "code": "password_too_short"
          },
          {
            "message": "This password is too common.",
            "code": "password_too_common"
          },
          {
            "message": "This password is entirely numeric.",
            "code": "password_entirely_numeric"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="Password mismatch"
{
  "data": {
    "passwordChange": {
      "success": false,
      "errors": {
        "newPassword2": [
          {
            "message": "The two password fields didn’t match.",
            "code": "password_mismatch"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

```bash tab="Invalid password"
{
  "data": {
    "passwordChange": {
      "success": false,
      "errors": {
        "oldPassword": [
          {
            "message": "Invalid password.",
            "code": "invalid_password"
          }
        ]
      },
      "token": null,
      "refreshToken": null
    }
  }
}
```

---

#### RemoveSecondaryEmail

{{ api.RemoveSecondaryEmail }}

```bash tab="graphql"
mutation {
  removeSecondaryEmail(
    password: "supersecretpassword"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "removeSecondaryEmail": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  removeSecondaryEmail(
    input: {
      password: "supersecretpassword"
    }
  ) {
    success,
    errors
  }
}
```

```bash tab="Invalid password"
{
  "data": {
    "removeSecondaryEmail": {
      "success": false,
      "errors": {
        "password": [
          {
            "message": "Invalid password.",
            "code": "invalid_password"
          }
        ]
      }
    }
  }
}
```

---

#### SendSecondaryEmailActivation

{{ api.SendSecondaryEmailActivation }}

```bash tab="graphql"
mutation {
  sendSecondaryEmailActivation(
    email: "my_secondary_email@email.com"
    password: "supersecretpassword",
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "sendSecondaryEmailActivation": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  sendSecondaryEmailActivation(
    input: {
      email: "my_secondary_email@email.com"
      password: "supersecretpassword",
    }
  ) {
    success,
    errors
  }
}
```


```bash tab="Unauthenticated"
{
  "data": {
    "sendSecondaryEmailActivation": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Unauthenticated.",
            "code": "unauthenticated"
          }
        ]
      }
    }
  }
}
```

```bash tab="Invalid email"
{
  "data": {
    "sendSecondaryEmailActivation": {
      "success": false,
      "errors": {
        "email": [
          {
            "message": "Enter a valid email address.",
            "code": "invalid"
          }
        ]
      }
    }
  }
}
```

```bash tab="Invalid password"
{
  "data": {
    "sendSecondaryEmailActivation": {
      "success": false,
      "errors": {
        "password": [
          {
            "message": "Invalid password.",
            "code": "invalid_password"
          }
        ]
      }
    }
  }
}
```

```bash tab="Not verified"
{
  "data": {
    "sendSecondaryEmailActivation": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Please verify your account."
            "code": "not_verified"
          }
        ]
      }
    }
  }
}
```

---

#### SwapEmails

{{ api.SwapEmails }}

```bash tab="graphql"
mutation {
  swapEmails(
    password: "supersecretpassword"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "swapEmails": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  swapEmails(
    input: {
      password: "supersecretpassword"
    }
  ) {
    success,
    errors
  }
}
```

```bash tab="Invalid password"
{
  "data": {
    "swapEmails": {
      "success": false,
      "errors": {
        "password": [
          {
            "message": "Invalid password.",
            "code": "invalid_password"
          }
        ]
      }
    }
  }
}
```

---

#### UpdateAccount

{{ api.UpdateAccount }}

```bash tab="graphql"
mutation {
  updateAccount(
    firstName: "Luke"
  ) {
    success,
    errors
  }
}
```

```bash tab="success"
{
  "data": {
    "updateAccount": {
      "success": true,
      "errors": null
    }
  }
}
```

```bash tab="relay"
mutation {
  updateAccount(
    input: {
      firstName: "Luke"
    }
  ) {
    success,
    errors
  }
}
```


```bash tab="Unauthenticated"
{
  "data": {
    "updateAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Unauthenticated.",
            "code": "unauthenticated"
          }
        ]
      }
    }
  }
}
```

```bash tab="Not verified"
{
  "data": {
    "updateAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Please verify your account."
            "code": "not_verified"
          }
        ]
      }
    }
  }
}
```
