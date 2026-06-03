from django.db import models

from accounts.models import Company


class Chatbot(models.Model):

    BOT_TYPES = [

        ("school", "School"),

        ("healthcare", "Healthcare"),

        ("ecommerce", "E-Commerce"),

        ("custom", "Custom"),
    ]


    company = models.ForeignKey(

        Company,

        on_delete=models.CASCADE,

        related_name="bots"
    )


    name = models.CharField(

        max_length=100
    )


    bot_type = models.CharField(

        max_length=50,

        choices=BOT_TYPES,

        default="custom"
    )


    description = models.TextField(

        blank=True
    )


    welcome_message = models.TextField(

        default="Hello! How can I help you today?"
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

        return self.name