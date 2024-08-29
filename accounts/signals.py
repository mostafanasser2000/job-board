from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile, CompanyProfile


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_company:
            CompanyProfile.objects.create(user=instance)
        else:
            UserProfile.objects.create(user=instance)
