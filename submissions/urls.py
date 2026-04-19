from django.urls import path
from .views import (
    SubmissionCreateView,
    SubmissionAdminListView,
    SubmissionAdminDetailView,
)

urlpatterns = [
    path("", SubmissionCreateView.as_view(), name="submission-create"),
    path("admin/", SubmissionAdminListView.as_view(), name="submission-admin-list"),
    path("admin/<int:pk>/", SubmissionAdminDetailView.as_view(), name="submission-admin-detail"),
]