from django.urls import path
from .views import PlatformListCreateView, PlatformDetailView

urlpatterns = [
    path("", PlatformListCreateView.as_view(), name="platform-list"),
    path("<slug:slug>/", PlatformDetailView.as_view(), name="platform-detail"),
]