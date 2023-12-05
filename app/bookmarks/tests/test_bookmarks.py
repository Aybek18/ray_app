import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from bookmarks.tests.factories import BookmarkFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
class TestBookmarkCreate:
    url = reverse("bookmark-create")

    def test_throw_error_if_access_token_invalid(self, api_client: APIClient) -> None:
        access_token = "NotValidAccessToken"
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token}")
        response = api_client.post(self.url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_requires_fields(self, api_client: APIClient, user: UserFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.post(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'url': ['This field is required.']}

    def test_requires_valid_value(self, api_client: APIClient, user: UserFactory) -> None:
        data = {"url": "It's not URL"}

        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "url": [
                "Enter a valid URL."
            ]
        }

    def test_return_404_if_url_doesnt_exist(self, api_client: APIClient, user: UserFactory) -> None:
        data = {"url": "https://www.unian.net/games/gta-6-nepravilniy_url"}

        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_creates_bookmark(self, api_client: APIClient, user: UserFactory) -> None:
        data = {"url": "https://www.unian.net/games/gta-6-pervyy-treyler-igra-vyydet-v-2025-godu-12475011.html"}

        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.post(self.url, data=data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_return_list_bookmarks(self, api_client: APIClient, user: UserFactory,
                                   bookmarks: [BookmarkFactory]) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{
            "id": bookmark.id,
            "created_at": bookmark.created_at.isoformat()[:-6] + 'Z',
            "updated_at": bookmark.updated_at.isoformat()[:-6] + 'Z',
            "page_title": bookmark.page_title,
            "description": bookmark.description,
            "page_url": bookmark.page_url,
            "page_type": bookmark.page_type.value,
            "image_url": bookmark.image_url,
            "user": user.id
        } for bookmark in bookmarks]


@pytest.mark.django_db
class TestBookmark:
    def get_url(self, bookmark_id: int = 12345):
        return reverse("bookmark", args=[bookmark_id])

    def test_throw_error_if_access_token_invalid(self, api_client: APIClient) -> None:
        access_token = "NotValidAccessToken"
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token}")
        response = api_client.get(self.get_url())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_return_404_bookmark_doesnt_exists(self, api_client: APIClient, user: UserFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.get(self.get_url())

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_bookmark_by_id(self, api_client: APIClient, user: UserFactory, bookmark: BookmarkFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.get(self.get_url(bookmark.id))

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": bookmark.id,
            "created_at": bookmark.created_at.isoformat()[:-6] + 'Z',
            "updated_at": bookmark.updated_at.isoformat()[:-6] + 'Z',
            "page_title": bookmark.page_title,
            "description": bookmark.description,
            "page_url": bookmark.page_url,
            "page_type": bookmark.page_type.value,
            "image_url": bookmark.image_url,
            "user": user.id
        }

    def test_change_bookmark_by_id(self, api_client: APIClient, user: UserFactory, bookmark: BookmarkFactory) -> None:
        data = {
            "description": "Change the description"
        }
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.patch(self.get_url(bookmark.id), data=data)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "id": bookmark.id,
            "created_at": bookmark.created_at.isoformat()[:-6] + 'Z',
            "updated_at": response.json().get("updated_at"),
            "page_title": bookmark.page_title,
            "description": data["description"],
            "page_url": bookmark.page_url,
            "page_type": bookmark.page_type.value,
            "image_url": bookmark.image_url,
            "user": user.id
        }

    def test_delete_bookmark_by_id(self, api_client: APIClient, user: UserFactory, bookmark: BookmarkFactory) -> None:
        access_token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {access_token.key}")
        response = api_client.delete(self.get_url(bookmark.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
