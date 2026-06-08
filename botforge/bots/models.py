from django.db import models

from accounts.models import Company
import uuid


class Chatbot(models.Model):

    BOT_TYPES = [

        ("school","School"),

        ("healthcare","Healthcare"),

        ("ecommerce","E-Commerce"),

        ("custom","Custom"),
    ]


    STATUS_CHOICES = [

        ("pending","Pending"),

        ("training","Training"),

        ("active","Active"),

        ("failed","Failed"),
    ]


    company = models.ForeignKey(

        Company,

        on_delete=models.CASCADE,

        related_name="bots"
    )


    name = models.CharField(
        max_length=100
    )


    website_url = models.URLField(
        blank=True,
        null=True
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


    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="pending"
    )


    last_crawled_at = models.DateTimeField(

        null=True,

        blank=True
    )


    auto_recrawl = models.BooleanField(
        default=True
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
    widget_key=models.UUIDField(
    default=uuid.uuid4,
    unique=True,
    editable=False
    )

    is_installed=models.BooleanField(
        default=False
    )

    installed_at=models.DateTimeField(
        null=True,
        blank=True
    )
    theme_color=models.CharField(
    max_length=20,
    default="#0d6efd"
    )

    widget_position=models.CharField(
        max_length=30,
        default="bottom-right"
    )
    is_deleted=models.BooleanField(
        default=False
    )

    deleted_at=models.DateTimeField(
        null=True,
        blank=True
    )
    
    


    def __str__(self):

        return self.name
    
    
class WebsitePage(models.Model):

    chatbot = models.ForeignKey(

        Chatbot,

        on_delete=models.CASCADE,

        related_name="pages"
    )

    url = models.URLField()

    title = models.CharField(
        max_length=500,
        blank=True
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    is_deleted=models.BooleanField(
    default=False
    )

    deleted_at=models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):

        return self.url
    
    
class WebsiteChunk(models.Model):

    chatbot = models.ForeignKey(
        Chatbot,
        on_delete=models.CASCADE,
        related_name="chunks",
        null=True,
        blank=True
    )

    page = models.ForeignKey(
        WebsitePage,
        on_delete=models.CASCADE,
        related_name="chunks",
        null=True,
        blank=True
    )

    source_type = models.CharField(
        max_length=50,
        default="website"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    chunk_text = models.TextField()

    embedding = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    source_id=models.PositiveIntegerField(
        null=True,
        blank=True
    )
    is_deleted=models.BooleanField(
        default=False
    )

    deleted_at=models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title or self.source_type
    
class BotKnowledge(models.Model):

    chatbot = models.ForeignKey(
        Chatbot,
        on_delete=models.CASCADE,
        related_name="knowledge_items"
    )

    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
    is_deleted=models.BooleanField(
    default=False
    )

    deleted_at=models.DateTimeField(
        null=True,
        blank=True
    )
    
class ChatSession(models.Model):

    chatbot=models.ForeignKey(
        Chatbot,
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )

    session_id=models.CharField(
        max_length=100,
        db_index=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    updated_at=models.DateTimeField(
        auto_now=True
    )
    is_deleted=models.BooleanField(
        default=False
    )

    deleted_at=models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.session_id
    
class ChatMessage(models.Model):

    SENDER_CHOICES=[
        ("user","User"),
        ("bot","Bot")
    ]

    session=models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender=models.CharField(
        max_length=10,
        choices=SENDER_CHOICES
    )

    message=models.TextField()

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.sender}"