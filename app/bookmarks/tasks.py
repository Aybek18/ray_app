from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from bookmarks.services import UpdateUserBookmarksService


@db_periodic_task(crontab(minute="*"))
def update_bookmark_data() -> None:
    """Task for checking bookmarks existence"""
    UpdateUserBookmarksService.update_all_bookmarks()
