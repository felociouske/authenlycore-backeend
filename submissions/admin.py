from django.contrib import admin
from .models import EvidenceSubmission, EvidenceFile


class EvidenceFileInline(admin.TabularInline):
    model = EvidenceFile
    extra = 0
    readonly_fields = ["file", "file_type", "caption", "uploaded_at"]


@admin.register(EvidenceSubmission)
class EvidenceSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        "id", "platform_label", "submitter_label",
        "amount_lost", "currency", "status", "submitted_at",
    ]
    list_filter = ["status"]
    search_fields = [
        "platform__name", "platform_name_raw",
        "submitter_email", "experience_description"
    ]
    list_editable = ["status"]
    ordering = ["-submitted_at"]
    inlines = [EvidenceFileInline]
    readonly_fields = ["submitted_at", "reviewed_at"]
    fieldsets = (
        ("Platform", {
            "fields": ("platform", "platform_name_raw", "platform_url_raw")
        }),
        ("Submitter", {
            "fields": ("submitter_name", "submitter_email", "is_anonymous")
        }),
        ("Details", {
            "fields": ("experience_description", "amount_lost", "currency")
        }),
        ("Moderation", {
            "fields": (
                "status", "admin_notes", "reviewed_by",
                "submitted_at", "reviewed_at"
            )
        }),
    )

    def platform_label(self, obj):
        return obj.platform.name if obj.platform else obj.platform_name_raw
    platform_label.short_description = "Platform"

    def submitter_label(self, obj):
        if obj.is_anonymous:
            return "Anonymous"
        return obj.submitter_name or obj.submitter_email or "Unknown"
    submitter_label.short_description = "Submitter"