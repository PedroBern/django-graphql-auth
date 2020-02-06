import django

import pytest


def skipif_django_21():
    return pytest.mark.skipif(
        django.get_version() < "2.2", reason="the custom model depends on 2.2"
    )
