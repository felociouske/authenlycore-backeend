from rest_framework import generics, filters, permissions
from django.utils import timezone
from accounts.permissions import IsAdminOrAuthor
from .models import BlogPost, Tag, BlogComment
from .serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    TagSerializer,
    BlogCommentSerializer,
)


class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrAuthor()]
        return [permissions.AllowAny()]


class BlogPostListCreateView(generics.ListCreateAPIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "body", "tags__name"]
    ordering_fields = ["published_at", "created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrAuthor()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = BlogPost.objects.select_related(
            "author"
        ).prefetch_related("tags")
        is_author = (
            self.request.user.is_authenticated
            and self.request.user.is_author
        )
        if not is_author:
            qs = qs.filter(is_published=True)
        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")
        featured = self.request.query_params.get("featured")
        if category:
            qs = qs.filter(category=category)
        if tag:
            qs = qs.filter(tags__slug=tag)
        if featured:
            qs = qs.filter(featured=True)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        if instance.is_published and not instance.published_at:
            instance.published_at = timezone.now()
            instance.save()


class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAdminOrAuthor()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = BlogPost.objects.select_related(
            "author"
        ).prefetch_related("tags", "comments__author")
        is_author = (
            self.request.user.is_authenticated
            and self.request.user.is_author
        )
        if not is_author:
            qs = qs.filter(is_published=True)
        return qs

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_published and not instance.published_at:
            instance.published_at = timezone.now()
            instance.save()


class BlogCommentCreateView(generics.CreateAPIView):
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = generics.get_object_or_404(
            BlogPost, slug=self.kwargs["slug"]
        )
        serializer.save(post=post)