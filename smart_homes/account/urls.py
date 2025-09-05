from django.urls import path
from smart_homes.account.views import RegisterUserView, LoginUserView, ProfileUserView, DeleteUserView, logout_user


urlpatterns = (
    path("register/", RegisterUserView.as_view(), name="register_user"),
    path("login/", LoginUserView.as_view(), name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    path("profile/<int:pk>/", ProfileUserView.as_view(), name="profile"),
    path("delete-profile/<int:pk>/", DeleteUserView.as_view(), name="delete_user"),
)
