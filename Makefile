.PHONY : pre-release check-release release test-local

release:
	python -m twine upload dist/* --verbose

pre-release:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel

check-release:
	python -m twine check dist/*

release: pre-release check-release release

test-local:
	tox -e py37-django30
