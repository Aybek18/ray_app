from typing import List

import pytest

from bookmarks.models import Bookmark
from bookmarks.tests.factories import BookmarkFactory


@pytest.fixture
def bookmarks(db, user) -> List[Bookmark]:
    bookmarks = BookmarkFactory.create_batch(size=5, user=user)
    return sorted(bookmarks, key=lambda x: x.created_at, reverse=True)


@pytest.fixture
def bookmark(db, bookmarks) -> Bookmark:
    return bookmarks[0]
