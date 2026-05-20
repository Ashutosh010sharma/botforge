from django.contrib import admin
from .models import Company

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'website_url',
        'industry',
        'is_active'
    )

    search_fields = (
        'company_name',
        'industry'
    )
