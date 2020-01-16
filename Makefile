.PHONY: tests
tests:
	py.test graphql_auth --cov=graphql_auth -vv

.PHONY: test
test: tests  # Alias test -> tests

.PHONY: release
release:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel
	python -m twine upload dist/* --verbose

.PHONY: test-local
test-local:
	tox -e py37-django30
