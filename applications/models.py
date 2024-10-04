from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from posts.models import JobPost
from core import choices_utils
from core.models import BaseModel
from django.urls import reverse


def upload_resume(instance, filename):
    return f"resumes/{instance.applicant.username}/{filename}"


def validate_resume_file_extension(value):
    valid_extensions = [".pdf", ".doc", ".docx"]
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(
            "Unsupported file extension. Please upload a PDF, DOC, or DOCX file."
        )


class Application(BaseModel):
    job_post = models.ForeignKey(
        JobPost, related_name="applications", on_delete=models.CASCADE, blank=True
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="applications",
        on_delete=models.CASCADE,
        blank=True,
    )
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(
        upload_to=upload_resume,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "doc", "docx"],
                message="Unsupported file extension. Please upload a PDF, DOC, or DOCX file.",
            ),
        ],
    )
    status = models.CharField(
        max_length=10,
        choices=choices_utils.APPLICATION_STATUS_CHOICES,
        default="pending",
        blank=True,
    )

    class Meta:
        unique_together = ("job_post", "applicant")
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.job_post.is_open:
            raise ValidationError("This Job is closed")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.applicant.username} Application for {self.job_post.title}"

    def get_absolute_url(self):
        return reverse(
            "application_detail",
            kwargs={
                "job_slug": self.job_post.slug,
                "username": self.applicant.username,
            },
        )
