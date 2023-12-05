from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from bookmarks.models import Bookmark
from bookmarks.serializers import BookmarkSerializer, BookmarkCreateSerializer
from bookmarks.services import BookmarkService


class BookmarkCreateAPIView(ListCreateAPIView):
    serializer_class = BookmarkCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        bookmark = BookmarkService.save_bookmark(url=serializer.validated_data["url"], user=user)
        return Response(BookmarkSerializer(bookmark).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        cached_data = cache.get(f"cached_bookmarks_{user.id}")
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)
        serializer = BookmarkSerializer(self.get_queryset(), many=True)
        cache.set(
            f"cached_bookmarks_{user.id}",
            serializer.data,
            timeout=settings.CACHE_EXPIRATION_SECONDS,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookmarkCreateSerializer
        elif self.request.method == "GET":
            return BookmarkSerializer


class BookmarkAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = (
        "get",
        "patch",
        "delete",
    )
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.all().filter(user=self.request.user)
