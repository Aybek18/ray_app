import factory
from factory.fuzzy import FuzzyText

from bookmarks.models import Bookmark
from users.tests.factories import UserFactory


class BookmarkFactory(factory.django.DjangoModelFactory):
    page_title = factory.Faker('sentence', nb_words=4)
    description = FuzzyText(length=100)
    page_url = factory.Faker("url")
    page_type = factory.fuzzy.FuzzyChoice(Bookmark.PageTypeEnum)
    image_url = factory.Faker("url")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Bookmark
