from django.contrib import admin
from .models import BlogPost, Tag, BlogComment


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    readonly_fields = ["author", "author_name", "created_at"]
    fields = ["author_name", "body", "status", "created_at"]


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "title", "author", "category",
        "featured", "is_published", "published_at"
    ]
    list_filter = ["is_published", "featured", "category"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published", "featured"]
    filter_horizontal = ["tags"]
    ordering = ["-created_at"]
    inlines = [BlogCommentInline]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author_name", "status", "created_at"]
    list_filter = ["status"]
    list_editable = ["status"]