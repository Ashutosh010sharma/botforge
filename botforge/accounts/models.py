import uuid

from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
   

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(
        max_length=200
    )

    website_url = models.URLField()

    industry = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    logo=models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.company_name