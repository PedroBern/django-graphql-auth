<!-- shameless copy from graphene-django CONTRIBUTING file -->

# Contributing

Thanks for helping improve Django GraphQL Auth!

All kinds of contributions are welcome:

- Bug fixes
- Documentation improvements
- New features
- Refactoring
- Fix some typo
- Write more tests

## Getting started

If you have a specific contribution in mind, be sure to check the [issues](https://github.com/PedroBern/django-graphql-auth/issues) and [projects](https://github.com/PedroBern/django-graphql-auth/projects) in progress - someone could already be working on something similar and you can help out.

## Project setup

After cloning this repo, ensure dependencies are installed by running:

```bash
make dev-setup
```

and

```bash
pip install tox
```

## Running tests

After developing, you can run tests with:

```bash
# python=3.7 and django=3.0
make test
```

You can specify versions, for the full list see the `tox.ini` file.

```bash
# python=3.6 and django=2.2
make test p=36 d=22
```

Test directly with tox:

```bash
tox
```

Single file test shortcut:

```bash
# run only tests in tests/test_register.py
make test-file f=register
```

For live testing on a django project, you can use the testproject.
 Create a different virtualenv, install the dependencies again and run:

```bash
cd testproject
make install-local v=<CURRENT VERSION IN graphql_auth.__init__>
```

## Opening Pull Requests

Please fork the project and open a pull request against the master branch.

This will trigger a series of tests and lint checks.

We advise that you format and run lint locally before doing this to save time:

```bash
make format
make lint
```

## Documentation

The documentation is generated using the excellent [MkDocs](https://www.mkdocs.org/) with [material theme](https://squidfunk.github.io/mkdocs-material/).

The documentation dependencies are installed by running:

```bash
pip install -r docs/requirements.txt
```

Then to produce a HTML version of the documentation, for live editing:

```bash
make serve
```

It will run the `docs/pre_build.py` script before building the docs.
