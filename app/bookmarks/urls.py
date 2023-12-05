from django.urls import path

from bookmarks.views import BookmarkCreateAPIView, BookmarkAPIView

urlpatterns = [
    path("", BookmarkCreateAPIView.as_view(), name="bookmark-create"),
    path("<int:pk>", BookmarkAPIView.as_view(), name="bookmark")
]