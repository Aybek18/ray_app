from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class UserAuthService:
    @classmethod
    def create_user(cls, user_data: dict) -> str:
        user = User.objects.create_user(**user_data)
        return cls.user_token(user)

    @classmethod
    def login_user(cls, user_data: dict) -> str:
        user = authenticate(**user_data)
        if not user:
            raise AuthenticationFailed()
        return cls.user_token(user)

    @classmethod
    def user_token(cls, user: User) -> str:
        access_token, _ = Token.objects.get_or_create(user=user)
        return access_token.key
