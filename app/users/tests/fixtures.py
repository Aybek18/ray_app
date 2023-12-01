import pytest

from app.users.models import User
from app.users.tests.factories import UserFactory


@pytest.fixture
def user(db) -> User:
    user = UserFactory.create()
    return user
