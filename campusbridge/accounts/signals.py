from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from support.models import AnonymousProfile

@receiver(post_save, sender=User)
def create_anon_profile(sender, instance, created, **kwargs):
    if created and instance.role == "student":
        AnonymousProfile.objects.get_or_create(user=instance)