from rest_framework import serializers

from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "age", "username")


class UserRegistrationSerializer(UserProfileSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = UserProfileSerializer.Meta.fields + ("password",)


class UserLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
