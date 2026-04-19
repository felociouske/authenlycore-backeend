from django.db import models
from django.conf import settings
from platforms.models import Platform


class EvidenceSubmission(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending Review"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    platform = models.ForeignKey(
        Platform,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="submissions"
    )
    platform_name_raw = models.CharField(max_length=200, blank=True)
    platform_url_raw = models.URLField(blank=True)

    submitter_name = models.CharField(max_length=150, blank=True)
    submitter_email = models.EmailField(blank=True)
    is_anonymous = models.BooleanField(default=False)

    experience_description = models.TextField()
    amount_lost = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=10, blank=True, default="USD")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_submissions",
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        label = (
            self.platform.name if self.platform
            else self.platform_name_raw
        )
        return f"Submission about '{label}' ({self.status})"


class EvidenceFile(models.Model):

    class FileType(models.TextChoices):
        IMAGE = "image", "Image"
        PDF = "pdf", "PDF"
        OTHER = "other", "Other"

    submission = models.ForeignKey(
        EvidenceSubmission,
        on_delete=models.CASCADE,
        related_name="files"
    )
    file = models.FileField(upload_to="evidence/")
    file_type = models.CharField(
        max_length=10,
        choices=FileType.choices,
        default=FileType.IMAGE
    )
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for submission #{self.submission.id}"