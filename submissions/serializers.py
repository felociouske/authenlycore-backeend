from rest_framework import serializers
from .models import EvidenceSubmission, EvidenceFile


class EvidenceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceFile
        fields = ["id", "file", "file_type", "caption", "uploaded_at"]


class EvidenceSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceSubmission
        fields = [
            "platform",
            "platform_name_raw",
            "platform_url_raw",
            "submitter_name",
            "submitter_email",
            "is_anonymous",
            "experience_description",
            "amount_lost",
            "currency",
        ]

    def validate_experience_description(self, value):
        if len(value.strip()) < 100:
            raise serializers.ValidationError(
                "Please provide at least 100 characters."
            )
        return value


class EvidenceSubmissionAdminSerializer(serializers.ModelSerializer):
    files = EvidenceFileSerializer(many=True, read_only=True)

    class Meta:
        model = EvidenceSubmission
        fields = "__all__"
        read_only_fields = ["submitted_at"]