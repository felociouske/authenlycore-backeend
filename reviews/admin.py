from django.contrib import admin
from .models import Review, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ["author", "author_name", "created_at"]
    fields = ["author_name", "body", "status", "created_at"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "title", "platform", "author",
        "is_published", "published_at", "created_at"
    ]
    list_filter = ["is_published", "platform__verdict", "platform__category"]
    search_fields = ["title", "body", "platform__name"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published"]
    ordering = ["-created_at"]
    inlines = [CommentInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["review", "author_name", "status", "created_at"]
    list_filter = ["status"]
    list_editable = ["status"]
    search_fields = ["body", "author_name"]