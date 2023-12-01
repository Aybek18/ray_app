import factory
from faker import Faker

from app.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("pystr")
    email = factory.Faker("email")
    age = Faker().date_of_birth(minimum_age=18, maximum_age=90).year
    password = factory.PostGenerationMethodCall("set_password", "password123")

    class Meta:
        model = User
