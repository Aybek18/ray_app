import pytest
from rest_framework.test import APIClient

pytest_plugins = [
    "users.tests.fixtures",
]


@pytest.fixture
def api_client():
    client = APIClient()
    return client
