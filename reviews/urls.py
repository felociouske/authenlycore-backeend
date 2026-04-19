from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    CommentCreateView,
)

urlpatterns = [
    path("", ReviewListCreateView.as_view(), name="review-list"),
    path("<slug:slug>/", ReviewDetailView.as_view(), name="review-detail"),
    path("<slug:slug>/comments/", CommentCreateView.as_view(), name="review-comment"),
]