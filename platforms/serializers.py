from rest_framework import serializers
from .models import Platform


class PlatformListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = [
            "id", "name", "slug", "category", "verdict",
            "overall_rating", "logo", "is_active", "created_at",
        ]


class PlatformDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = "__all__"