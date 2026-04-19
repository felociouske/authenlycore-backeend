from django.urls import path
from .views import (
    BlogPostListCreateView,
    BlogPostDetailView,
    TagListView,
    BlogCommentCreateView,
)

urlpatterns = [
    path("", BlogPostListCreateView.as_view(), name="blog-list"),
    path("tags/", TagListView.as_view(), name="tag-list"),
    path("<slug:slug>/", BlogPostDetailView.as_view(), name="blog-detail"),
    path("<slug:slug>/comments/", BlogCommentCreateView.as_view(), name="blog-comment"),
]