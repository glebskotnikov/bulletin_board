from django.conf import settings
from django.db import models


class Ad(models.Model):
    title = models.CharField(max_length=200, verbose_name="title")
    price = models.IntegerField(verbose_name="price")
    description = models.TextField(verbose_name="description")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="author",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created at"
    )

    class Meta:
        verbose_name = "abs"
        verbose_name_plural = "abs"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="text")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="author",
    )
    ad = models.ForeignKey(
        Ad,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="advertisement",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="created at"
    )

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"
        ordering = ["-created_at"]

    def __str__(self):
        return self.text
