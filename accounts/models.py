from django.db import models
from django.contrib.auth.models import AbstractUser
from profiles.models import UserProfile


class CustomUser(AbstractUser):
    is_company = models.BooleanField(
        blank=True,
        default=False,
        help_text="Designates wether a user can post jobs or not",
    )
