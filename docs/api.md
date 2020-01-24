# API

---

## Mutations

### Basics

#### Import

All of the following can be imported like this:

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

#### Standard response

All mutations will return a standard response containing `#!python errors` and `#!python success`.

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
    errors
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
      }
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
    errors
  }
}
```

---

### Register

Register account with [optional](/settings/#register_mutation_fields_optional) and [required](/settings/#register_mutation_fields) fields defined in settings.

- Success example

```bash tab="graphql"
mutation {
  register(
    email:"skywalker@email.com",
    username:"skywalker",
    password1: "qlr4nq3f3",
    password2:"qlr4nq3f3"
  ) {
    success, errors
  }
}
```

```bash tab="response"
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
  register(
    input: {
      email:"skywalker@email.com",
      username:"skywalker",
      password1: "qlr4nq3f3",
      password2:"qlr4nq3f3"
    }
  ) {
    success, errors
  }
}
```

- Fail examples

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
      }
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
      }
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
      }
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
      }
    }
  }
}
```

---

### UpdateAccount

Update account with fields defined in [settings](/settings/#update_mutation_fields).


---

### ResendActivationEmail

Send a new activation email.

Note that will return `#!python success=True` even if email does not exist, but return `#!python success=False` if user with the email exist and the server can't send the email.

- Success example

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

```bash tab="response"
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

- Fail examples

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
        "email": [
          [
            {
              "message": "Failed to send email.",
              "code": "email_fail"
            }
          ]
        ]
      }
    }
  }
}
```

---

### VerifyAccount

Try to verify account.

- Success example

```bash tab="graphql"
mutation {
  verifyAccount(
    token:"eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6ImFjdGl2YXRpb24ifQ:1itC5A:vJhRJwBcrNxvmEKxHrZa6Yoqw5Q",
  ) {
    success, errors
  }
}
```

```bash tab="response"
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
  verifyAccount(
    input: {
      token:"eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImFjdGlvbiI6ImFjdGl2YXRpb24ifQ:1itC5A:vJhRJwBcrNxvmEKxHrZa6Yoqw5Q",
    }
  ) {
    success, errors
  }
}
```

- Fail examples

```bash tab="Invalid token"
{
  "data": {
    "verifyAccount": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid or expirated token.",
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

### ArchiveAccount

Archive account. User must be logged-in and confirm the password. It will make
`#!python user.is_active=False` and revoke all user tokens on the database (if
  using [long running refresh tokens](https://django-graphql-jwt.domake.io/en/latest/refresh_token.html#long-running-refresh-tokens)).

- Success example

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

```bash tab="response"
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

- Fail examples

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

---

### DeleteAccount

Delete account permanently. User must be logged-in and confirm the password.

- Success example

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

```bash tab="response"
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

- Fail examples

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

---

### PasswordChange

Change user password. User must be logged-in and confirm the password. It will
revoke all user tokens on the database (if
  using [long running refresh tokens](https://django-graphql-jwt.domake.io/en/latest/refresh_token.html#long-running-refresh-tokens)).

Return `#!python success=False` if:

- User is not logged in
- Fail to confirm password
- Fail on password validators

---

### PasswordReset

Reset user password. It will
revoke all user tokens on the database (if
  using [long running refresh tokens](https://django-graphql-jwt.domake.io/en/latest/refresh_token.html#long-running-refresh-tokens)).

- Success example

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

```bash tab="response"
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


- Fail examples

```bash tab="Invalid token"
{
  "data": {
    "passwordReset": {
      "success": false,
      "errors": {
        "nonFieldErrors": [
          {
            "message": "Invalid or expirated token.",
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

### SendPasswordResetEmail

Send password reset email.

Note that will return `#!python success=True` even if email does not exist, but return `#!python success=False` if user with the email exist and the server can't send the email.

- Success example

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

```bash tab="response"
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

- Fail examples

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
        "email": [
          [
            {
              "message": "Failed to send email.",
              "code": "email_fail"
            }
          ]
        ]
      }
    }
  }
}
```

---

### Authentication

These mutations are built with [GraphQL JWT](https://github.com/flavors/django-graphql-jwt/).

Most cases we are simply wrapping the original class to return the [standard response](/api/#standard-response).

---

#### ObtainJSONWebToken

If user is archived, it means:

```python
archived = user.is_active == False and user.last_login
```

Then, the user becomes active again on login.

If try to send more than one field deffined in [LOGIN_ALLOWED_FIELDS](/settings/#login_allowed_fields), will raise.

- Success example

```bash tab="graphql"
mutation {
  tokenAuth(
    # user username or email
    email: "skywalker@email.com"
    password: "123456super"
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

```bash tab="response"
{
  "data": {
    "tokenAuth": {
      "success": true,
      "errors": null,
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImV4cCI6MTU3OTQ1ODI2Niwib3JpZ0lhdCI6MTU3OTQ1Nzk2Nn0.BKz4ohxQCGtJWnyd5tIbYFD2kpGYDiAVzWTDO2ZyUYY",
      "refreshToken": "5f5fad67cd043437952ddde2750be20201f1017b",
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

- Fail examples

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
      "user": null
    }
  }
}
```

```bash tab="Wrong usage"
{
  "errors": [
    {
      "message": "Must login with password and one of the following fields ['email', 'username'].",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "tokenAuth"
      ]
    }
  ],
  "data": {
    "tokenAuth": null
  }
}
```

---

#### VerifyToken

- Success example

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

```bash tab="response"
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

- Fail examples

```bash tab="Invalid token"
{
  "data": {
    "verifyToken": {
      "success": false,
      "errors": {
        "token": [
          {
            "message": "Invalid or expirated token.",
            "code": "invalid_token"
          }
        ]
      },
      "payload": null
    }
  }
}
```

---

#### RefreshToken

- Success example

```bash tab="graphql"
mutation {
  refreshToken(
    refreshToken: "ab6e297efddda056f3a6207ee12303329c577349"
  ) {
    success,
    errors,
    payload
    token,
    refreshToken,
  }
}
```

```bash tab="response"
{
  "data": {
    "refreshToken": {
      "success": true,
      "errors": null,
      "payload": {
        "username": "skywalker",
        "exp": 1579459012,
        "origIat": 1579458712
      },
      "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNreXdhbGtlciIsImV4cCI6MTU3OTQ1OTAxMiwib3JpZ0lhdCI6MTU3OTQ1ODcxMn0.61kbfSxATCV1WcLN_DCE6hSHfnRyR_hIHl0HbZR65B8",
      "refreshToken": "d9b58dce41cf14549030873e3fab3be864f76ce4"
    }
  }
}
```

```bash tab="relay"
mutation {
  refreshToken(
    input: {
      refreshToken: "ab6e297efddda056f3a6207ee12303329c577349"
    }
  ) {
    success,
    errors,
    payload
    token,
    refreshToken,
  }
}
```

- Fail examples

```bash tab="Invalid token"
{
  "data": {
    "refreshToken": {
      "success": false,
      "errors": {
        "refreshToken": [
          {
            "message": "Invalid or expirated token.",
            "code": "invalid_token"
          }
        ]
      },
      "payload": null,
      "token": null,
      "refreshToken": null
    }
  }
}
```

---

#### RevokeToken

- Success example

```bash tab="graphql"
mutation {
  revokeToken(
    refreshToken: "d9b58dce41cf14549030873e3fab3be864f76ce44"
  ) {
    success,
    errors,
    revoked
  }
}
```

```bash tab="response"
{
  "data": {
    "revokeToken": {
      "success": true,
      "errors": null,
      "revoked": 1579458880
    }
  }
}
```

```bash tab="relay"
mutation {
  revokeToken(
    input: {
      refreshToken: "d9b58dce41cf14549030873e3fab3be864f76ce44"
    }
  ) {
    success,
    errors,
    revoked
  }
}
```

- Fail examples

```bash tab="Invalid token"
{
  "data": {
    "revokeToken": {
      "success": false,
      "errors": {
        "refreshToken": [
          {
            "message": "Invalid or expirated token.",
            "code": "invalid_token"
          }
        ]
      },
      "revoked": null
    }
  }
}
```
