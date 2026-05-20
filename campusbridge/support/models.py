from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

User=get_user_model()




class AnonymousProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    anon_id=models.CharField(max_length=20,unique=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.anon_id:
            self.anon_id = f"ANON-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
            return self.anon_id




class SupportRequest(models.Model):
    anonymous_profile=models.ForeignKey(AnonymousProfile,on_delete=models.CASCADE)

    title=models.CharField(max_length=200)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

