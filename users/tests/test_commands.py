import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

User = get_user_model()


@pytest.mark.django_db
def test_create_superuser_command():
    """
    Test the 'csu' command for creating a superuser
    with predefined characteristics.
    """
    assert User.objects.count() == 0
    call_command("csu")
    assert User.objects.count() == 1

    user = User.objects.first()

    assert user.email == "admin@yandex.ru"
    assert user.first_name == "Admin"
    assert user.last_name == "Skypro"
    assert user.is_superuser is True
    assert user.is_staff is True
    assert user.is_active is True
    assert user.check_password("123qwe456rty") is True
