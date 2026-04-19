from rest_framework import generics, filters, permissions
from django.utils import timezone
from accounts.permissions import IsAdminOrAuthor
from .models import Review, Comment
from .serializers import (
    ReviewListSerializer,
    ReviewDetailSerializer,
    CommentSerializer,
)


class ReviewListCreateView(generics.ListCreateAPIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "body", "platform__name"]
    ordering_fields = ["published_at", "created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewDetailSerializer
        return ReviewListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrAuthor()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Review.objects.select_related("platform", "author")
        is_author = (
            self.request.user.is_authenticated
            and self.request.user.is_author
        )
        if not is_author:
            qs = qs.filter(is_published=True)
        verdict = self.request.query_params.get("verdict")
        category = self.request.query_params.get("category")
        if verdict:
            qs = qs.filter(platform__verdict=verdict)
        if category:
            qs = qs.filter(platform__category=category)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        if instance.is_published and not instance.published_at:
            instance.published_at = timezone.now()
            instance.save()


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAdminOrAuthor()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = Review.objects.select_related(
            "platform", "author"
        ).prefetch_related("comments__author")
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


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        review = generics.get_object_or_404(
            Review, slug=self.kwargs["slug"]
        )
        serializer.save(review=review)