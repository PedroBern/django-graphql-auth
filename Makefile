.PHONY: release
release:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel
	python -m twine upload dist/* --verbose

.PHONY: test-local
test-local:
	tox -e py37-django30
