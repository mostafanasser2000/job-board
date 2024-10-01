from django.db import models
from django.utils.text import slugify
from django.core.validators import URLValidator
from core import choices_utils
from core.models import BaseModel, Industry, Skill, Country
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse


def upload_profile_image(instance, filename):
    return f"{'photos' if isinstance(instance, UserProfile) else 'logos'}/{instance.user.username}/{filename}"


class Profile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(class)s"
    )
    name = models.CharField(max_length=255)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_profile_image, blank=True, null=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contact_email = models.EmailField(null=True, blank=True)

    facebook_url = models.URLField(validators=[URLValidator], null=True, blank=True)
    twitter_url = models.URLField(validators=[URLValidator], null=True, blank=True)
    linkedin_url = models.URLField(validators=[URLValidator], null=True, blank=True)
    website = models.URLField(validators=[URLValidator], null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name or self.user.username} Profile"
    
    def get_absolute_url(self):
        url = "company_profile" if user.is_company else "user_profile"
        return reverse(url, kwargs={"username": self.user.username})
    
    def get_social_links(self):
        return {
            field.name.split("_url")[0]: getattr(self, field.name)
            for field in self._meta.fields
            if field.name.endswith("_url") and getattr(self, field.name)
        }

    @property
    def logo(self):
        if self.image:
            return self.image.url
        return f"{'static/imgs/logo.svg' if self.user.is_company else 'static/imgs/avatar.png'}"

    @property
    def str_name(self):
        return f"{self.name or self.user.username}"

class UserProfile(Profile):
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=choices_utils.GENDER_CHOICES, null=True, blank=True
    )
    military_status = models.CharField(
        max_length=20,
        choices=choices_utils.MILITARY_STATUS_CHOICES,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse("user_profile", kwargs={"username": self.user.username})


class CompanyProfile(Profile):
    slug = models.SlugField(blank=True, unique=True)
    industries = models.ManyToManyField(Industry, null=True, blank=True)
    founded_at = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:

            if not CompanyProfile.objects.filter(slug=slugify(self.name)).exists():
                self.slug = slugify(self.name)
            else:
                self.slug = self.slug = slugify(f"{self.name}-{self.id}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("company_profile", kwargs={"company": self.slug})


class Education(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="educations", on_delete=models.CASCADE
    )

    degree = models.CharField(max_length=100, choices=choices_utils.DEGREE_CHOICES)
    institution_name = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ["-end_date"]

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be greater than start date.")

    def __str__(self):
        return f"{self.degree} at {self.institution_name} ({self.start_date.year} - {self.end_date.year})"

    @property
    def date_range(self):
        start = self.start_date.strftime("%b %Y")
        end = self.end_date.strftime("%b %Y")
        return f"{start} - {end}"


class UserSkill(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="skills", on_delete=models.CASCADE
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "skill")

    def __str__(self) -> str:
        return f"{self.skill.name}"


class Experience(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="experiences", on_delete=models.CASCADE
    )
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    job_category = models.ManyToManyField(Industry, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        if self.is_current and self.end_date:
            raise ValidationError("Current experience cannot have an end date.")
        if not self.is_current and not self.end_date:
            raise ValidationError("Please provide an end date for this experience.")
        if self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be greater than start date.")

    def __str__(self):
        return f"{self.job_title} at ({self.company_name})"

    @property
    def date_range(self):
        start = self.start_date.strftime("%b %Y")
        if self.is_current:
            return f"{start} - Present"
        elif self.end_date:
            end = self.end_date.strftime("%b %Y")
            return f"{start} - {end}"
