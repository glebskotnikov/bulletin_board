import pytest
from django.contrib.auth import get_user_model

from ads.models import Ad, Review
from ads.views import AdViewSet, ReviewViewSet

User = get_user_model()


@pytest.fixture
def test_ad(test_user, db):
    return Ad.objects.create(
        title="Test Ad",
        price=100,
        description="Ad description",
        author=test_user,
    )


@pytest.fixture
def test_admin_ad(test_admin_user, db):
    return Ad.objects.create(
        title="Test Ad",
        price=100,
        description="Ad description",
        author=test_admin_user,
    )


@pytest.fixture
def test_review(test_user, test_ad, db):
    return Review.objects.create(
        text="Test Review", author=test_user, ad=test_ad
    )


@pytest.fixture
def test_user(db):
    user = User.objects.create(
        email="user@test.com", first_name="first", last_name="last"
    )
    user.set_password("testpass")
    user.save()
    return user


@pytest.fixture
def test_admin_user(db):
    admin_user = User.objects.create(
        email="admin@test.com",
        first_name="first",
        last_name="last",
        is_staff=True,
    )
    admin_user.set_password("testpass")
    admin_user.save()
    return admin_user


@pytest.fixture
def ad_view_set():
    return AdViewSet()


@pytest.fixture
def review_view_set():
    return ReviewViewSet()
