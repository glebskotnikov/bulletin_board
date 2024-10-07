from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.test import APIRequestFactory, force_authenticate

from ads.views import AdViewSet, ReviewViewSet

User = get_user_model()
factory = APIRequestFactory()


def test_ad_view_set_list(ad_view_set, test_user, test_admin_user, test_ad):
    """
    Tests the successful retrieval of Ad listings in AdViewSet list view.
    """
    request = factory.get("/fake-path/")
    force_authenticate(request, user=test_user)
    ad_list_view = AdViewSet.as_view({"get": "list"})
    response = ad_list_view(request)
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Test Ad"


def test_ad_view_set_retrieve(ad_view_set, test_user, test_admin_user, test_ad):
    """
    Tests successful retrieval of a specific Ad in AdViewSet retrieve view.
    """
    request = factory.get("/fake-path/")
    force_authenticate(request, user=test_user)
    ad_retrieve_view = AdViewSet.as_view({"get": "retrieve"})
    response = ad_retrieve_view(request, pk=test_ad.pk)
    assert response.status_code == 200
    assert response.data["title"] == "Test Ad"


def test_ad_view_set_get_permissions_list(ad_view_set):
    """
    Ensure that the 'get_permissions' method for
    the 'list' action is being used.
    """
    ad_view_set.action = "list"
    permissions = ad_view_set.get_permissions()
    assert len(permissions) > 0
    assert isinstance(permissions[0], AllowAny)


def test_ad_view_set_get_permissions_retrieve(ad_view_set):
    """
    Ensure that the 'get_permissions' method for
    the 'retrieve' action is being used.
    """
    ad_view_set.action = "retrieve"
    permissions = ad_view_set.get_permissions()
    assert len(permissions) > 0
    assert isinstance(permissions[0], IsAuthenticated)


def test_review_view_set_get_permissions_list_and_retrieve(review_view_set):
    """
    Ensure that the 'get_permissions' method for the 'list'
    and 'retrieve' actions is being used.
    """
    for action in ["list", "retrieve"]:
        review_view_set.action = action
        permissions = review_view_set.get_permissions()
        assert len(permissions) > 0
        assert isinstance(permissions[0], IsAuthenticated)


def test_ad_view_set_create(ad_view_set, test_user):
    """
    Tests successful creation of an Ad by
    an authenticated user via AdViewSet 'create' view.
    """
    request = factory.post(
        "/fake-path/", data={"title": "Test", "price": 100, "description": "Test"}
    )
    force_authenticate(request, user=test_user)
    ad_create_view = AdViewSet.as_view({"post": "create"})
    response = ad_create_view(request)
    assert response.status_code == 201
    assert response.data["title"] == "Test"
    assert "author" in response.data


def test_review_view_set_create(review_view_set, test_user, test_ad):
    """
    Tests successful creation of a Review by
    an authenticated user via the ReviewViewSet 'create' view.
    """
    request = factory.post(
        "/fake-path/", data={"text": "Review Test", "ad": test_ad.id}
    )
    force_authenticate(request, user=test_user)
    review_create_view = ReviewViewSet.as_view({"post": "create"})
    response = review_create_view(request)
    assert response.status_code == 201
    assert response.data["text"] == "Review Test"
    assert "author" in response.data
