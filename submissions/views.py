from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from accounts.permissions import IsAdminOnly
from .models import EvidenceSubmission, EvidenceFile
from .serializers import (
    EvidenceSubmissionCreateSerializer,
    EvidenceSubmissionAdminSerializer,
    EvidenceFileSerializer,
)


class SubmissionCreateView(generics.CreateAPIView):
    serializer_class = EvidenceSubmissionCreateSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        files = request.FILES.getlist("files")
        for uploaded_file in files[:5]:
            file_type = "image"
            if uploaded_file.content_type == "application/pdf":
                file_type = "pdf"
            EvidenceFile.objects.create(
                submission=submission,
                file=uploaded_file,
                file_type=file_type,
                caption=request.data.get(
                    f"caption_{uploaded_file.name}", ""
                ),
            )

        return Response(
            {"detail": "Submission received. Thank you."},
            status=status.HTTP_201_CREATED,
        )


class SubmissionAdminListView(generics.ListAPIView):
    serializer_class = EvidenceSubmissionAdminSerializer
    permission_classes = [IsAdminOnly]

    def get_queryset(self):
        qs = EvidenceSubmission.objects.select_related(
            "platform", "reviewed_by"
        ).prefetch_related("files")
        submission_status = self.request.query_params.get(
            "status", "pending"
        )
        return qs.filter(status=submission_status)


class SubmissionAdminDetailView(generics.RetrieveUpdateAPIView):
    queryset = EvidenceSubmission.objects.all()
    serializer_class = EvidenceSubmissionAdminSerializer
    permission_classes = [IsAdminOnly]

    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user,
            reviewed_at=timezone.now(),
        )