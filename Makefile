.PHONY : test-local test-local-file serve build-docs check-readme install-local

check-readme:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel
	python -m twine check dist/*

install-local:
	rm -rf dist build django_graphql_auth.egg-info
	python setup.py sdist bdist_wheel
	python -m pip install dist/django-graphql-auth-${v}.tar.gz

p ?= 37
d ?= 30

test-local:
	tox -e py${p}-django${d} -- --cov-report term-missing --cov-report html

test-local-file:
	tox -e py${p}-django${d} -- tests/test_${f}.py --cov-report html --cov-append

serve:
	mkdocs serve

build-docs:
	mkdocs build
