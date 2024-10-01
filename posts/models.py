from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from django.conf import settings
from core import choices_utils
from core.models import BaseModel
from core.models import Currency, Country, Skill
from django.core.validators import FileExtensionValidator
from django.db.models import Manager


class JobPostManager(Manager):
    @property
    def opened(self):
        return self.filter(status="opened")

    @property
    def closed(self):
        return self.filter(status="closed")


def upload_resume(instance, filename):
    return f"resumes/{instance.applicant.username}/{filename}"


def validate_resume_file_extension(value):
    valid_extensions = [".pdf", ".doc", ".docx"]
    if not any(value.name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(
            "Unsupported file extension. Please upload a PDF, DOC, or DOCX file."
        )


class JobPost(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500, unique=True, blank=True)
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="jobs", on_delete=models.CASCADE
    )
    description = RichTextField()
    skills_required = models.ManyToManyField(Skill, related_name="jobs")
    workplace_type = models.CharField(
        max_length=20, choices=choices_utils.WORKPLACE_TYPES
    )
    work_type = models.CharField(max_length=20, choices=choices_utils.WORK_TYPES)
    start_salary = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    end_salary = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True, blank=True
    )
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True, related_name="jobs"
    )
    status = models.CharField(
        max_length=10,
        choices=choices_utils.JOB_STATUS_CHOICES,
        default="opened",
        blank=True,
    )
    objects = JobPostManager()

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["title", "publisher"]),
            models.Index(fields=["-created"]),
        ]

    def clean(self):
        if self.start_salary and self.end_salary:
            if self.end_salary < self.start_salary:
                raise ValidationError(
                    "End salary must be greater than or equal to start salary."
                )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f"{self.title}-at-{self.publisher}-{self.pk}")
            super().save(update_fields=["slug"])

    def __str__(self):
        return f"{self.title} at {self.publisher}"

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"slug": self.slug})

    @property
    def salary_range(self):
        salary_text = ""
        if self.start_salary and self.end_salary:
            salary_text = f"{self.start_salary}-{self.end_salary}"
        elif self.start_salary:
            salary_text = f"From {self.start_salary}"
        elif self.end_salary:
            salary_text = f"Up to {self.end_salary}"

        return (
            f'{salary_text} {self.currency.code or "USD"}'
            if salary_text
            else "Not specified"
        )

    @property
    def location(self):
        return self.country.name or "Fully Remote"

    @property
    def is_open(self):
        return self.status == "opened"


