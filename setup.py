#!/usr/bin/env python

import io
import os
import re
from collections import OrderedDict

from setuptools import find_packages, setup


def get_long_description():
    for filename in ("README.rst",):
        with io.open(filename, "r", encoding="utf-8") as f:
            yield f.read()


def get_version(package):
    with io.open(os.path.join(package, "__init__.py")) as f:
        pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
        return re.search(pattern, f.read(), re.MULTILINE).group(1)


tests_require = [
    "pytest>=3.6.3",
    "pytest-cov>=2.4.0",
    "pytest-django>=3.1.2",
    "coveralls",
]

setup(
    name="django-graphql-auth",
    version=get_version("graphql_auth"),
    license="MIT",
    description="Graphql and relay authentication with Graphene for Django.",
    long_description="\n\n".join(get_long_description()),
    long_description_content_type="text/markdown",
    author="pedrobern",
    author_email="pedrobermoreira@gmail.com",
    maintainer="pedrobern",
    url="https://github.com/PedroBern/django-graphql-auth",
    project_urls=OrderedDict(
        (("Issues", "https://github.com/PedroBern/django-graphql-auth/issues"),)
    ),
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "Django>=2.1.0",
        "django-graphql-jwt>=0.3.0",
        "django-filter>=2.2.0",
        "graphene_django>=2.1.8",
        "graphene>=2.1.8",
    ],
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
    ],
    keywords="api graphql rest relay graphene auth",
    zip_safe=False,
    include_package_data=True,
    extras_require={"test": tests_require, "dev": tests_require,},
)
