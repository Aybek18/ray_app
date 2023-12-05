import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserLogin:
    url = reverse("user-login")

    def test_requires_fields(self, api_client: APIClient) -> None:
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "username": [
                "This field is required."
            ],
            "password": [
                "This field is required."
            ]
        }

    def test_requires_valid_data(self, api_client: APIClient) -> None:
        data = {"username": "wrong_username", "password": "wrong_password"}

        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {
            "detail": "Incorrect authentication credentials."
        }

    def test_return_access_token(self, api_client: APIClient, user: UserFactory) -> None:
        data = {"username": user.username, "password": "password123"}

        response = api_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["access_token"]


@pytest.mark.django_db
class TestUserRegistration:
    url = reverse("user-registration")

    def test_requires_fields(self, api_client: APIClient) -> None:
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "age": [
                "This field is required."
            ],
            "username": [
                "This field is required."
            ]
        }

    def test_check_for_uniqueness_of_fields(self, api_client: APIClient, user: UserFactory) -> None:
        data = {
            "first_name": "Lionel",
            "last_name": "Messi",
            "email": user.email,
            "age": 36,
            "username": user.username,
            "password": "password"
        }

        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "email": [
                "user with this email already exists."
            ],
            "username": [
                "A user with that username already exists."
            ]
        }

    def test_check_for_email_field(self, api_client: APIClient) -> None:
        data = {
            "first_name": "Lionel",
            "last_name": "Messi",
            "email": "It is not Email",
            "age": 36,
            "username": "Lionel_Messi",
            "password": "password"
        }

        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "email": [
                "Enter a valid email address."
            ]
        }

    def test_return_access_token(self, api_client: APIClient) -> None:
        data = {
            "first_name": "Lionel",
            "last_name": "Messi",
            "email": "lm10@gmail.com",
            "age": 36,
            "username": "Lionel_Messi",
            "password": "password"
        }

        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["access_token"]


@pytest.mark.django_db
class TestUserLogout:
    url = reverse("user-logout")

    def test_throw_error_if_access_token_invalid(self, api_client: APIClient) -> None:
        access_token = "NotValidAccessToken"
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token}")
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_logout(self, api_client: APIClient, user: UserFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUserProfile:
    url = reverse("user-profile")

    def test_throw_error_if_access_token_invalid(self, api_client: APIClient) -> None:
        access_token = "NotValidAccessToken"
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token}")
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_retrieve(self, api_client: APIClient, user: UserFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "username": user.username
        }

    def test_user_update(self, api_client: APIClient, user: UserFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        update_data = {
            "first_name": "Cristiano",
            "last_name": "Ronaldo",
            "email": "cr7@gmail.com",
            "age": 38,
            "username": "cristiano_ronaldo"
        }
        response = api_client.patch(self.url, data=update_data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_delete(self, api_client: APIClient, user: UserFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.delete(self.url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
