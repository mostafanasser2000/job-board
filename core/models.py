from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, URLValidator


class Company(models.Model):
    COMPANY_SIZE_CHOICES = [
        (1, "1-10"),
        (2, "11-50"),
        (3, "51-200"),
        (4, "201-500"),
        (5, "501-1000"),
        (6, "1001+"),
    ]
    logo = models.ImageField(upload_to="companies/%Y/%m/%d/")
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    company_site = models.URLField(blank=True, null=True, validators=[URLValidator()])
    location = models.CharField(max_length=200)
    about = models.TextField(null=True, blank=True)
    company_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        choices=COMPANY_SIZE_CHOICES,
        validators=[MinValueValidator(1)],
    )
    linkedin_page = models.URLField(blank=True, null=True, validators=[URLValidator()])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_related_jobs(self):
        return Job.objects.filter(skills_required=self)


class Job(models.Model):
    WORKPLACE_TYPES = [
        ("Remote", "Remote"),
        ("Hybrid", "Hybrid"),
        ("On-site", "On-site"),
    ]

    WORK_TYPES = [
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    ]
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
        # Add more as needed
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, blank=True)
    company = models.ForeignKey(Company, related_name="jobs", on_delete=models.CASCADE)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, related_name="jobs")
    workplace_type = models.CharField(max_length=20, choices=WORKPLACE_TYPES)
    work_type = models.CharField(max_length=20, choices=WORK_TYPES)
    location = models.CharField(max_length=200)
    salary_lowest = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    salary_highest = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    salary_currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    apply_link = models.URLField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["title", "company", "location"])]

    def clean(self):
        if self.salary_highest and self.salary_lowest:
            if self.salary_highest < self.salary_lowest:
                raise models.ValidationError(
                    "Highest salary must be greater than or equal to lowest salary."
                )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.company.name}-{self.location}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})
