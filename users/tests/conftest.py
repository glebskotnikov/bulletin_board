# /tests/conftest.py
import pytest
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "test@example.com",
        "password": "testpass1234",
        "first_name": "First",
        "last_name": "Last",
        "phone": "+1234567890",
        "role": "user",
    }


@pytest.fixture
def user(db, user_data):
    password = user_data.pop("password")
    user = User.objects.create(**user_data)
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def token():
    return PasswordResetTokenGenerator()


@pytest.fixture
def password_reset_confirm_data(user, token):
    return {
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": token.make_token(user),
        "new_password": "newpass1234",
    }
