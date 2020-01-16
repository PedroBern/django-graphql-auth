.PHONY : pre-release check-release release test-local lint-rst

release:
	python -m twine upload dist/* --verbose

pre-release:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel

check-release:
	python -m twine check dist/*

lint-rst:
	rst-lint README.rst

release: lint-rst pre-release check-release release

test-local:
	tox -e py37-django30
