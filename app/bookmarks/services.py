from typing import List

import requests
from bs4 import BeautifulSoup
from requests import Response
from rest_framework.exceptions import NotFound, ParseError

from bookmarks.models import Bookmark
from users.models import User


class BookmarkService:
    @classmethod
    def save_bookmark(cls, url: str, user: User) -> Bookmark:
        page_title, description, image_url, page_url, page_type = cls.get_data(url)
        instance = Bookmark.objects.create(page_title=page_title, description=description, image_url=image_url,
                                           page_url=page_url,
                                           page_type=page_type, user=user)
        return instance

    @classmethod
    def get_data(cls, url: str) -> [str]:
        """For parsing HTML and extracting content-meta tags. """
        response = cls.request_data(url=url)
        if response.status_code == 404:
            raise NotFound()
        try:
            raw_data = BeautifulSoup(response.content, "html.parser")
            page_title = raw_data.find("meta", property="og:title")["content"]
            description = raw_data.find("meta", property="og:description")["content"]
            image_url = raw_data.find("meta", property="og:image")["content"]
            page_url = raw_data.find("meta", property="og:url")["content"]
            page_type = raw_data.find("meta", property="og:type")["content"]

            # checking page type
            checked_page_type = cls.check_page_type(page_type=page_type)

        except Exception as e:
            raise ParseError()
        return page_title, description, image_url, page_url, checked_page_type

    @classmethod
    def request_data(cls, url: str) -> Response:
        """Request Data from given URL"""
        return requests.get(url=url)

    @classmethod
    def check_page_type(cls, page_type: str) -> str:
        """Check for page type. If page type not in choices than by default return "website" value"""
        allowed_page_types = [choice[0] for choice in Bookmark.PageTypeEnum.choices]
        if page_type in allowed_page_types:
            return page_type.lower()
        return Bookmark.PageTypeEnum.WEBSITE.value


class UpdateUserBookmarksService:

    @classmethod
    def get_all_bookmarks(cls) -> List[Bookmark]:
        return Bookmark.objects.all()

    @classmethod
    def update_all_bookmarks(cls) -> None:
        """Check for validness of page_url, if url doesn't exist anymore than it will be deleted"""
        bookmarks = cls.get_all_bookmarks()
        count = 0
        for bookmark in bookmarks:
            response = BookmarkService.request_data(bookmark.page_url)
            if response.status_code == 404:
                bookmark.delete()
                count += 1

        print(f"{count} закладок было удалено")
