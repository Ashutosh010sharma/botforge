from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(SchoolKnowledge)
class SchoolKnowledgeAdmin(
    admin.ModelAdmin
):

    list_display = (

        "title",
        "created_at"
    )

    search_fields = (

        "title",
        "content"
    )

admin.site.register(
    SchoolKnowledgeChunk
)