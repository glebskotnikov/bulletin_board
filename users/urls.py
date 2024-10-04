from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PasswordResetConfirmView, PasswordResetView,
                         RegisterUserView)

app_name = UsersConfig.name

urlpatterns = [
    # users
    path("register/", RegisterUserView.as_view(), name="register"),
    path("reset_password/", PasswordResetView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/",
        PasswordResetConfirmView.as_view(),
        name="reset_password_confirm",
    ),
    # token
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
