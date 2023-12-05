from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from bookmarks.models import Bookmark


@receiver([post_delete, post_save], sender=Bookmark)
def clear_cache_on_model_modification(sender, instance, **kwargs):
    user_id = instance.user.id
    cache_key = f"cached_bookmarks_{user_id}"
    cache.delete(cache_key)
