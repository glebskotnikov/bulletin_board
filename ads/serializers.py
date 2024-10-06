from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ad, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email")


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "text", "author", "ad", "created_at"]


class AdSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ["id", "title", "price", "description", "author", "created_at"]


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "price",
            "description",
            "author",
            "created_at",
            "reviews",
        ]
