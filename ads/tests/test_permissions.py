from rest_framework.test import APIRequestFactory

from ads.permissions import IsOwnerOrAdmin

factory = APIRequestFactory()


def test_is_owner_or_admin_author(test_user, test_ad):
    """
    Test that if the user is the author of the object,
    has_object_permission returns True.
    """
    request = factory.get("/fake-path/")
    request.user = test_user
    permission = IsOwnerOrAdmin()
    assert permission.has_object_permission(request, None, test_ad)


def test_is_owner_or_admin_staff(test_admin_user, test_ad):
    """
    Test that if the user is an administrator,
    has_object_permission returns True, even if they are not the author.
    """
    request = factory.get("/fake-path/")
    request.user = test_admin_user
    permission = IsOwnerOrAdmin()
    assert permission.has_object_permission(request, None, test_ad)


def test_is_owner_or_admin_not_author_or_staff(test_user, test_admin_ad):
    """
    Test that if the user is neither the author nor an administrator,
    has_object_permission returns False.
    """
    request = factory.get("/fake-path/")
    request.user = test_user
    permission = IsOwnerOrAdmin()
    assert not permission.has_object_permission(request, None, test_admin_ad)
