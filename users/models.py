from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    first_name = models.CharField(max_length=50, verbose_name="first name")
    last_name = models.CharField(max_length=50, verbose_name="last name")
    phone = models.CharField(max_length=35, verbose_name="phone", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="email")
    role = models.CharField(
        max_length=10,
        choices=(("user", "User"), ("admin", "Admin")),
        default="user",
    )
    image = models.ImageField(
        upload_to="users/", verbose_name="avatar", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["email"]

    def __str__(self):
        return self.email
