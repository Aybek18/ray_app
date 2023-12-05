from rest_framework import serializers

from bookmarks.models import Bookmark


class BookmarkCreateSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = (
            "id",
            "created_at",
            "updated_at",
            "page_title",
            "description",
            "page_url",
            "page_type",
            "image_url",
            "user",
        )
        read_only_fields = (
            "user",
        )
