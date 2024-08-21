from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, URLValidator
from django.utils import timezone
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Industry(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


# class Location(BaseModel):
#     city = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.city}, {self.country}"


class Company(BaseModel):
    COMPANY_SIZE_CHOICES = [
        (1, "1-10"),
        (2, "11-50"),
        (3, "51-200"),
        (4, "201-500"),
        (5, "501-1000"),
        (6, "1001+"),
    ]
    logo = models.ImageField(upload_to="media/companies/%Y/%m/%d/")
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    company_site = models.URLField(blank=True, null=True, validators=[URLValidator()])
    about = models.TextField(null=True, blank=True)
    company_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        choices=COMPANY_SIZE_CHOICES,
        validators=[MinValueValidator(1)],
    )
    linkedin_page = models.URLField(blank=True, null=True, validators=[URLValidator()])
    industries = models.ManyToManyField(Industry, related_name="companies")
    # location = models.ForeignKey(
    #     Location, on_delete=models.SET_NULL, null=True, related_name="companies"
    # )

    class Meta:
        ordering = ["-created"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})

    def total_employees(self):
        return self.COMPANY_SIZE_CHOICES[self.company_size][1]

    def get_open_positions(self):
        pass


class Skill(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_related_jobs(self):
        return Job.objects.filter(skills_required=self)

    @property
    def related_jobs_count(self):
        return self.jobs.count()


# class JobManager(models.Manager):
#     def active(self):
#         return self.filter(status="published")

#     def by_skill(self, skill):
#         return self.filter(skills_required=skill)


class Job(BaseModel):
    # STATUS = [
    #     ("draft", "Draft"),
    #     ("published", "Published"),
    #     ("closed", "Closed"),
    # ]
    WORKPLACE_TYPES = [
        ("remote", "Remote"),
        ("hybrid", "Hybrid"),
        ("on-site", "On-site"),
    ]

    WORK_TYPES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
    ]
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    company = models.ForeignKey(Company, related_name="jobs", on_delete=models.CASCADE)
    description = models.TextField()
    skills_required = models.ManyToManyField(Skill, related_name="jobs")
    workplace_type = models.CharField(max_length=20, choices=WORKPLACE_TYPES)
    work_type = models.CharField(max_length=20, choices=WORK_TYPES)
    # location = models.ForeignKey(
    #     Location, on_delete=models.SET_NULL, null=True, related_name="jobs"
    # )
    salary_lowest = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    salary_highest = models.PositiveIntegerField(
        blank=True, null=True, validators=[MinValueValidator(0)]
    )
    salary_currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, default="USD"
    )
    apply_link = models.URLField(blank=True, null=True, validators=[URLValidator()])

    # objects = JobQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["title", "company"]),
            models.Index(fields=["-created"]),
        ]

    def clean(self):
        if self.salary_highest and self.salary_lowest:
            if self.salary_highest < self.salary_lowest:
                raise ValidationError(
                    "Highest salary must be greater than or equal to lowest salary."
                )

    def save(self, *args, **kwargs):
        if not self.slug:
            super().save(*args, **kwargs)
            self.slug = slugify(f"{self.title}-{self.company.name}-{self.id}")
            super().save(update_fields=["slug"])
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})

    @property
    def salary_range(self):
        if self.salary_lowest and self.salary_highest:
            return (
                f"{self.salary_lowest} - {self.salary_highest} {self.salary_currency}"
            )
        elif self.salary_lowest:
            return f"From {self.salary_lowest} {self.salary_currency}"
        elif self.salary_highest:
            return f"Up to {self.salary_highest} {self.salary_currency}"
        else:
            return "Not specified"

    @classmethod
    def get_recent_jobs(cls, days=7):
        # return cls.objects.active().filter(
        #     created__gte=timezone.now() - timezone.timedelta(days=days)
        # )
        pass

    def apply_to_job(self, user):
        pass
