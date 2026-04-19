from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor.fields import RichTextField
import math


class Tag(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):

    class Category(models.TextChoices):
        INVESTIGATION = "investigation", "Investigation"
        SCAM_ALERT = "scam_alert", "Scam Alert"
        LEGIT_SITE = "legit_site", "Legit Site"
        GUIDE = "guide", "Guide & Tips"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=320, unique=True, blank=True)
    body = RichTextField()
    cover_image = models.ImageField(
        upload_to="blog_covers/", blank=True, null=True
    )
    category = models.CharField(max_length=30, choices=Category.choices)
    tags = models.ManyToManyField(
        Tag, blank=True, related_name="posts"
    )
    is_published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def reading_time_minutes(self):
        word_count = len(self.body.split())
        return max(1, math.ceil(word_count / 200))

    def __str__(self):
        return self.title


class BlogComment(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    author_name = models.CharField(max_length=100, blank=True)
    body = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment on '{self.post.title}'"