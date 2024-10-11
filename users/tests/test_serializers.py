import pytest
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers

from users.serializers import (PasswordResetConfirmSerializer,
                               PasswordResetSerializer)


@pytest.mark.django_db
def test_password_reset_serializer_save(user):
    """
    Test the validity of the PasswordResetSerializer
    and its ability to send a password reset email.
    """
    serializer = PasswordResetSerializer(data={"email": user.email})
    assert serializer.is_valid()
    serializer.save()
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == "Password Reset"
    assert mail.outbox[0].to == [user.email]


@pytest.mark.django_db
def test_password_reset_confirm_serializer_save(
    user, password_reset_confirm_data
):
    """
    Test the PasswordResetConfirmSerializer's validity
    and its ability to change the user's password.
    """
    serializer = PasswordResetConfirmSerializer(
        data=password_reset_confirm_data
    )
    assert serializer.is_valid()
    new_password = "newpass1234"
    assert user.check_password(new_password) is False
    serializer.save()
    user.refresh_from_db()
    assert user.check_password(new_password)


@pytest.mark.django_db
def test_password_reset_confirm_serializer_invalid_uid():
    """
    Test the PasswordResetConfirmSerializer's behavior
    when provided with an invalid user id (uid)
    and check that it raises a validation error.
    """
    invalid_data = {
        "uid": "invalid",
        "token": "token",
        "new_password": "new_password",
    }
    serializer = PasswordResetConfirmSerializer(data=invalid_data)
    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
    assert "uid" in exc_info.value.detail
    assert exc_info.value.detail["uid"][0] == "Invalid value"


@pytest.mark.django_db
def test_password_reset_confirm_serializer_invalid_token(user, token):
    """
    Test the PasswordResetConfirmSerializer's behavior
    when provided with an invalid token
    and check that it raises a validation error.
    """
    invalid_data = {
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": "invalid",
        "new_password": "new_password",
    }
    serializer = PasswordResetConfirmSerializer(data=invalid_data)
    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.is_valid(raise_exception=True)
    assert "token" in exc_info.value.detail
    assert exc_info.value.detail["token"][0] == "Invalid value"
