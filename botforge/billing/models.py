from django.db import models
from accounts.models import Company


class Plan(models.Model):

    name=models.CharField(
        max_length=100
    )

    slug=models.SlugField(
        unique=True
    )

    monthly_price=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    max_bots=models.PositiveIntegerField(
        default=1
    )

    max_pages=models.PositiveIntegerField(
        default=10
    )

    max_messages=models.PositiveIntegerField(
        default=100
    )

    is_active=models.BooleanField(
        default=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.name


class Subscription(models.Model):

    company=models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="subscription"
    )

    plan=models.ForeignKey(
        Plan,
        on_delete=models.PROTECT
    )

    is_active=models.BooleanField(
        default=True
    )

    start_date=models.DateTimeField(
        auto_now_add=True
    )

    end_date=models.DateTimeField(
        null=True,
        blank=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.company.company_name} - {self.plan.name}"