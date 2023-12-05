from django.urls import path

from users.views import UserLoginAPIView, UserRegistrationAPIView, UserLogout, UserProfileAPIView

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("registration/", UserRegistrationAPIView.as_view(), name="user-registration"),
    path("logout/", UserLogout.as_view(), name="user-logout"),
    path("", UserProfileAPIView.as_view(), name="user-profile"),

]