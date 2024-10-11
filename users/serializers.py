import os.path

from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from config import settings

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "role",
            "image",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise ValidationError("User with given email does not exist")
        return value

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # create reset password url
        domain = "http://localhost:8000"
        reset_password_url = f"{domain}/change-password/{uid}/{token}"

        # load email template
        message = render_to_string(
            os.path.join(
                settings.BASE_DIR, "templates/users/password_reset_email.html"
            ),
            {"user": user, "reset_password_url": reset_password_url},
        )

        send_mail("Password Reset", message, None, [email])


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data["uid"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {
                    "uid": ["Invalid value"],
                }
            )

        if not default_token_generator.check_token(user, data["token"]):
            raise serializers.ValidationError(
                {
                    "token": ["Invalid value"],
                }
            )

        password_validation.validate_password(data["new_password"], user)

        return data

    def save(self):
        new_password = self.validated_data["new_password"]
        uid = force_str(urlsafe_base64_decode(self.validated_data["uid"]))
        user = User.objects.get(pk=uid)
        user.set_password(new_password)
        user.save()
        return user
