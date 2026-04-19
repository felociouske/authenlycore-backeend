from django.db import models
from django.utils.text import slugify


class Platform(models.Model):

    class Category(models.TextChoices):
        MLM = "mlm", "MLM / Network Marketing"
        CRYPTO = "crypto", "Crypto / Investment"
        SURVEY = "survey", "Survey / GPT"
        FREELANCE = "freelance", "Freelance / Remote Work"
        FOREX = "forex", "Forex / Trading"
        DROPSHIP = "dropship", "Dropshipping / E-commerce"
        APP = "app", "App / Mobile Task"
        OTHER = "other", "Other"

    class Verdict(models.TextChoices):
        SCAM = "scam", "Scam"
        LEGITIMATE = "legitimate", "Legitimate"
        SUSPICIOUS = "suspicious", "Suspicious"
        UNVERIFIED = "unverified", "Unverified"

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    website_url = models.URLField(blank=True)
    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.OTHER
    )
    verdict = models.CharField(
        max_length=20,
        choices=Verdict.choices,
        default=Verdict.UNVERIFIED
    )
    overall_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0
    )
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to="platform_logos/", blank=True, null=True
    )
    country_of_origin = models.CharField(max_length=100, blank=True)
    date_founded = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name