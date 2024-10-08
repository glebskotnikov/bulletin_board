import pytest
from django.contrib.auth import get_user_model

from ads.models import Ad, Review
from users.models import User


def test_ad_title_content(test_ad):
    """
    Test the title content of an advertisement.
    """
    assert str(test_ad.title) == "Test Ad"


def test_ad_author_content(test_ad):
    """
    Test the author content of an advertisement.
    """
    assert str(test_ad.author) == "user@test.com"


def test_review_text_content(test_review):
    """
    Test the text content of a review.
    """
    assert str(test_review.text) == "Test Review"


def test_review_author_content(test_review):
    """
    Test the author content of a review.
    """
    assert str(test_review.author) == "user@test.com"


def test_user_exists(test_user):
    """
    Test that a user exists.
    """
    assert User.objects.filter(email=test_user.email).exists()


def test_ad_exists(test_ad):
    """
    Test that an advertisement exists.
    """
    assert Ad.objects.filter(title=test_ad.title).exists()


def test_review_exists(test_review):
    """
    Test that a review exists.
    """
    assert Review.objects.filter(text=test_review.text).exists()


def test_ad_length_limit(test_user, db):
    """
    Test the length limit of an advertisement title.
    """
    long_string = "a" * 201
    with pytest.raises(Exception):
        Ad.objects.create(
            title=long_string,
            price=100,
            description="Ad description",
            author=test_user,
        )


def test_unique_user(test_user, db):
    """
    Test that a user's email is unique.
    """
    with pytest.raises(Exception):
        get_user_model().objects.create(
            email="user@test.com", first_name="second", last_name="last"
        )


def test_user_deletion_cascades(test_user, db):
    """
    Test that when a user is deleted, all their ads are deleted.
    """
    test_ad = Ad.objects.create(
        title="Test Ad",
        price=100,
        description="Ad description",
        author=test_user,
    )
    test_user.delete()
    assert not Ad.objects.filter(title=test_ad.title).exists()


def test_ad_ordering(test_user, db):
    """
    Test that advertisements are ordered correctly.
    """
    first_ad = Ad.objects.create(
        title="First",
        price=100,
        description="Ad description",
        author=test_user,
    )
    second_ad = Ad.objects.create(
        title="Second",
        price=100,
        description="Ad description",
        author=test_user,
    )
    assert list(Ad.objects.all()) == [second_ad, first_ad]


def test_review_ordering(test_user, test_ad, db):
    """
    Test that reviews are ordered correctly.
    """
    first_review = Review.objects.create(
        text="First Review", author=test_user, ad=test_ad
    )
    second_review = Review.objects.create(
        text="Second Review", author=test_user, ad=test_ad
    )
    assert list(Review.objects.all()) == [second_review, first_review]


def test_ad_str_method(test_ad):
    """
    Test the ad's string representation method.
    """
    assert test_ad.__str__() == "Test Ad"


def test_review_str_method(test_review):
    """
    Test the review's string representation method.
    """
    assert test_review.__str__() == "Test Review"
