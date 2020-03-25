# Changelog

## v0.3


### v0.3.6

- Replace RemovedInDjango40Warning ugettext with gettext (thanks to [ulgens](https://github.com/ulgens))

### v0.3.5

- Added `MeQuery` (thanks to [pors](https://github.com/pors)).

### v0.3.4

- Renamed from `ErrorType` to`ExpectedErrorType`, preventing clash with a `graphene_django` type with same name..

### v0.3.3

- Fixed bug when performing login in `PasswordChangeMixin` (thanks to [panosangelopoulos](https://github.com/panosangelopoulos)).

### v0.3.2

- Fixed typo in error code/message for `expired_token` (thanks to [yanivtoledano](https://github.com/yanivtoledano)).

### v0.3.1

- add pk to UserNode.

### v0.3.0

- release beta.

## v0.2

### v0.2.8

- return new token and refreshToken on password change.

### v0.2.7

- allow login on register, returning token and refresh token.

### v0.2.6

- review error fields in some mutations.

### v0.2.5

- update apps config.
- nothing new.

### v0.2.4

- add mutation to remove secondary email.

### v0.2.3

- user status is created on signal.

### v0.2.2

- fix typo in setup.
- nothing new.

### v0.2.1

- fix readme on pypi.
- nothing new.

### v0.2.0

- minor bug fixes.
- add user status model to track if user is archived, verified and secondary email.
- add new mutations to handle secondary email.
- allow login with secondary email.

## v0.1

### 0.1.11

- Fix minor bugs.

### 0.1.10

- Fix minor bugs.

### 0.1.9

- Rename settings params.

### 0.1.8

- Fix typo in settings.

### 0.1.7

- No changes (testing release on Travis).

### 0.1.6

- Support for Django >= 2.1

### 0.1.5

- Revoke refresh tokens when archiving user.

### 0.1.4

- Allow to revoke refresh tokens on password change and reset.

### 0.1.3

- Better settings api.

### 0.1.2

- Update setup.py.

### 0.1.1

- Add initial README file!

### 0.1.0

- Hello world!
