from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from users.services import UserAuthService


class UserRegistrationAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        responses={201: OpenApiResponse(description='{"access_token": "Your access Token"}')})
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = UserAuthService.create_user(serializer.validated_data)
        return Response(data={"access_token": access_token}, status=status.HTTP_201_CREATED)


class UserLoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = UserAuthService.login_user(serializer.validated_data)
        return Response(data={"access_token": access_token}, status=status.HTTP_200_OK)


class UserLogout(APIView):

    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_204_NO_CONTENT)


class UserProfileAPIView(RetrieveUpdateDestroyAPIView):
    http_method_names = (
        "get",
        "patch",
        "delete",
    )
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
