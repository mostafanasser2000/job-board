from django.db import models
from django.utils.text import slugify


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


class Country(BaseModel):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.name) != self.slug:
            self.slug = slugify(self.name)
        super().save(*args, *kwargs)


class City(BaseModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    country = models.ForeignKey(
        Country, related_name="cities", on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        if not self.slug or slugify(self.name) != self.slug:
            self.slug = slugify(self.name)
        super().save(*args, *kwargs)


class Currency(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
