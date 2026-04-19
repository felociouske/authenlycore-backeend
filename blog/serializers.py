from rest_framework import serializers
from .models import BlogPost, Tag, BlogComment
from accounts.serializers import UserPublicSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class BlogCommentSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = BlogComment
        fields = ["id", "author", "author_name", "body", "created_at"]
        read_only_fields = ["author"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
            validated_data["author_name"] = request.user.username
        return super().create(validated_data)


class BlogPostListSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time_minutes = serializers.ReadOnlyField()

    class Meta:
        model = BlogPost
        fields = [
            "id", "author", "title", "slug", "cover_image",
            "category", "tags", "featured", "published_at",
            "reading_time_minutes", "meta_description",
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        source="tags",
        write_only=True
    )
    comments = BlogCommentSerializer(many=True, read_only=True)
    reading_time_minutes = serializers.ReadOnlyField()

    class Meta:
        model = BlogPost
        fields = [
            "id", "author", "title", "slug", "body", "cover_image",
            "category", "tags", "tag_ids", "featured",
            "is_published", "published_at", "meta_description",
            "reading_time_minutes", "created_at", "updated_at", "comments",
        ]
        read_only_fields = ["author", "slug"]