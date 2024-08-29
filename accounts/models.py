from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.utils.text import slugify
from django.core.validators import URLValidator, RegexValidator, MinValueValidator
from core import choices_utils
from core.models import Country, City, BaseModel, Currency, Industry


def upload_profile_image(instance, filename):
    if isinstance(instance, UserProfile):
        return f"photos/{instance.user.username}/{filename}"

    return f"logos/{instance.user.username}/{filename}"


class CustomUser(AbstractUser):
    is_company = models.BooleanField(
        blank=True,
        default=False,
        help_text="Designates wether a user can post jobs or not",
    )


class Profile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_profile_image, blank=True, null=True)

    class Meta:
        abstract = True


class UserProfile(Profile):
    def __str__(self) -> str:
        return f"{self.user.username} Profile"


class CompanyProfile(Profile):
    name = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        if self.name:
            return f'{self.name} Company Profile'
        return f'{self.user.username} Company Profile'
