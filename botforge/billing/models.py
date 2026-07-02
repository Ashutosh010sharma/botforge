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
    yearly_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True
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

    BILLING_CHOICES = (

        ("monthly", "Monthly"),

        ("yearly", "Yearly"),

    )

    company = models.OneToOneField(

        Company,

        on_delete=models.CASCADE,

        related_name="subscription"

    )

    plan = models.ForeignKey(

        Plan,

        on_delete=models.PROTECT

    )

    payment = models.ForeignKey(

        "Payment",

        on_delete=models.SET_NULL,

        null=True,

        blank=True,

        related_name="subscriptions"

    )

    billing_cycle = models.CharField(

        max_length=20,

        choices=BILLING_CHOICES,

        default="monthly"

    )

    is_active = models.BooleanField(

        default=True

    )

    auto_renew = models.BooleanField(

        default=False
    )

    cancel_at_period_end = models.BooleanField(

        default=False

    )

    renewal_count = models.PositiveIntegerField(

        default=0

    )

    start_date = models.DateTimeField(null=True,
        blank=True,)

    end_date = models.DateTimeField(null=True,
        blank=True,)

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        return f"{self.company.company_name} - {self.plan.name}"
    
    
class Payment(models.Model):

    STATUS_CHOICES = [

        ("created", "Created"),
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
        ("refunded", "Refunded"),

    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    razorpay_order_id = models.CharField(
        max_length=150,
        unique=True
    )

    razorpay_payment_id = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    razorpay_signature = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="created"
    )

    gateway_response = models.JSONField(
        blank=True,
        null=True
    )

    failure_reason = models.TextField(
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(fields=["razorpay_order_id"]),

            models.Index(fields=["razorpay_payment_id"]),

            models.Index(fields=["status"]),

            models.Index(fields=["company"]),

        ]

    def __str__(self):

        return f"{self.company.company_name} - {self.razorpay_order_id}"