.PHONY : pre-release check-release release test-local lint-rst serve build-docs check-readme

release:
	python -m twine upload dist/* --verbose

pre-release:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel

check-release:
	python -m twine check dist/*

check-readme:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel
	python -m twine check dist/*

lint-rst:
	rst-lint README.rst

release: pre-release check-release release

test-local:
	tox -e py37-django30

serve:
	mkdocs serve

build-docs:
	mkdocs build
