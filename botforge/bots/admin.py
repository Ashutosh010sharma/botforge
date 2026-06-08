from django.contrib import admin

# Register your models here.
from .models import Chatbot,WebsitePage,WebsiteChunk,BotKnowledge,ChatMessage,ChatSession


admin.site.register(
    Chatbot
)
admin.site.register(
    WebsitePage
)
admin.site.register(
    WebsiteChunk
)
admin.site.register(
    BotKnowledge
)
admin.site.register(
    ChatSession
)
admin.site.register(
    ChatMessage
)