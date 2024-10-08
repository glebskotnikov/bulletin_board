import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
def test_register_user_view(api_client, user_data):
    """
    Test user registration view by asserting successful
    creation and correct email assignment.
    """
    url = reverse("users:register")
    response = api_client.post(url, data=user_data)
    assert response.status_code == HTTP_201_CREATED
    assert response.data["user"]["email"] == user_data["email"]


@pytest.mark.django_db
def test_password_reset_view_invalid_email(api_client, user):
    """
    Test password reset view with invalid email to assert error response.
    """
    url = reverse("users:reset_password")
    response = api_client.post(url, data={"email": "invalid" + user.email})
    assert response.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_reset_view(api_client, user):
    """
    Test password reset view with valid email to assert success response.
    """
    url = reverse("users:reset_password")
    response = api_client.post(url, data={"email": user.email})
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_password_reset_confirm_view(
    api_client, user, password_reset_confirm_data
):
    """
    Test password reset confirmation view to assert success response.
    """
    url = reverse("users:reset_password_confirm")
    response = api_client.post(url, data=password_reset_confirm_data)
    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_register_user_view_bad_request(api_client):
    """
    Test user registration view with invalid data
    to assert receiving a bad request response.
    """
    url = reverse("users:register")
    invalid_data = {"username": "test", "password": 2}
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_reset_view_bad_request(api_client):
    """
    Test password reset view with invalid email data
    to assert bad request response.
    """
    url = reverse("users:reset_password")
    invalid_data = {"email": 2}
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_password_reset_confirm_view_bad_request(api_client):
    """
    Test password reset confirmation view with invalid token data
    to assert bad request response.
    """
    url = reverse("users:reset_password_confirm")
    invalid_data = {"token": 2, "new_password": "asd123!"}
    response = api_client.post(url, data=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
