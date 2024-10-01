from django.db import models
from django.utils.text import slugify
import re


def custom_slug(value):
    value = value.replace('+', 'plus').replace('#', 'sharp')
    slug = slugify(value)
    if not slug:
        slug = re.sub(r'[^\w\s-]', '', value.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-_')
    return slug


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Industry(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=300, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug != slugify(self.name):
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'{self.name} ({self.code})'


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slug(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(blank=True, unique=True, db_index=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
