from django.db import models

from core.models import TimestampedModel
from users.models import User


class Bookmark(TimestampedModel):
    class PageTypeEnum(models.TextChoices):
        """Link Type"""
        WEBSITE = "website", "website"
        BOOK = "book", "book"
        ARTICLE = "article", "article"
        MUSIC = "music", "music"
        VIDEO = "video", "video"

    page_title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    page_url = models.URLField(max_length=255)
    page_type = models.CharField(max_length=7, choices=PageTypeEnum.choices, default=PageTypeEnum.WEBSITE.value)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_collections")
