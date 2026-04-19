from rest_framework import serializers
from .models import Review, Comment
from accounts.serializers import UserPublicSerializer
from platforms.serializers import PlatformListSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "author_name", "body", "created_at"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
            validated_data["author_name"] = request.user.username
        return super().create(validated_data)


class ReviewListSerializer(serializers.ModelSerializer):
    platform = PlatformListSerializer(read_only=True)
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "platform", "author", "title", "slug",
            "rating_transparency", "rating_payout", "rating_support",
            "is_published", "published_at", "meta_description",
        ]


class ReviewDetailSerializer(serializers.ModelSerializer):
    platform = PlatformListSerializer(read_only=True)
    platform_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__("platforms").models.Platform.objects.all(),
        source="platform",
        write_only=True,
    )
    author = UserPublicSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "platform", "platform_id", "author",
            "title", "slug", "body",
            "rating_transparency", "rating_payout", "rating_support",
            "is_published", "published_at", "meta_description",
            "created_at", "updated_at", "comments",
        ]
        read_only_fields = ["author", "slug"]