from django.contrib import admin
from .models import Platform


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = [
        "name", "category", "verdict",
        "overall_rating", "is_active", "created_at"
    ]
    list_filter = ["verdict", "category", "is_active"]
    search_fields = ["name", "website_url", "description"]
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ["verdict", "is_active"]
    ordering = ["-created_at"]