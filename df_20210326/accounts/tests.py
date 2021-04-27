from django.conf import settings

import pytest

from accounts.models import create_database, list_databases

pytestmark = pytest.mark.django_db


def test_custom_user_model():
    assert settings.AUTH_USER_MODEL == "accounts.User"


def test_database_created():
    db_list = list_databases()
    assert not db_list
    create_database('user_1', 'password1')
    db_list = list_databases()
    assert db_list == ['user_1']
