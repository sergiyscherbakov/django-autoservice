from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматичне створення профілю при створенні користувача"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Автоматичне збереження профілю при збереженні користувача"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
