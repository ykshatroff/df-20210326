from unittest import mock

from django.conf import settings

import pytest
from django.db import transaction
from django.urls import reverse
from model_bakery import baker

from rest_framework.test import APIClient

from accounts.models import create_database, list_databases, User, database_exists

# pytestmark = pytest.mark.django_db
from accounts.rest.views import DemoAdminUserView


def test_custom_user_model():
    assert settings.AUTH_USER_MODEL == "accounts.User"


@pytest.mark.django_db(transaction=True)
def test_database_created():
    db_list = list_databases()
    assert not db_list
    assert not database_exists("user_1")
    create_database("user_1", "password1")
    db_list = list_databases()
    assert db_list == [("user_1", "user_1")]
    assert database_exists("user_1")


@pytest.mark.django_db(transaction=True)
def test_user_create_view():
    user: User = baker.make(User, id=777, database="user_777", database_password="password777")

    client = APIClient()
    client.force_authenticate(user)

    response = client.get(reverse("api-demo-admin"))
    assert response.status_code == 200
    assert response.data == {"data": [], "status": "ok"}

    response = client.post(reverse("api-demo-admin"), {"name": "new_user", "active": True})

    assert response.status_code == 201
    assert response.data == {
        "data": {"id": mock.ANY, "name": "new_user", "active": True, "password": mock.ANY, "created_at": mock.ANY},
        "status": "ok",
    }
