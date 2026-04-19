from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from accounts.permissions import IsAdminOnly
from .models import Platform
from .serializers import PlatformListSerializer, PlatformDetailSerializer


class PlatformListCreateView(generics.ListCreateAPIView):
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description", "website_url"]
    ordering_fields = ["overall_rating", "created_at", "name"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PlatformDetailSerializer
        return PlatformListSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOnly()]
        return [IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        qs = Platform.objects.all()
        verdict = self.request.query_params.get("verdict")
        category = self.request.query_params.get("category")
        if verdict:
            qs = qs.filter(verdict=verdict)
        if category:
            qs = qs.filter(category=category)
        return qs


class PlatformDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformDetailSerializer
    lookup_field = "slug"

    def get_permissions(self):
        if self.request.method in ("PUT", "PATCH", "DELETE"):
            return [IsAdminOnly()]
        return [IsAuthenticatedOrReadOnly()]