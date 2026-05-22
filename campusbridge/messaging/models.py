from django.db import models
from django.contrib.auth import get_user_model
from support.models import AnonymousProfile
User = get_user_model()


class Conversation(models.Model):
    anonymous_profile = models.ForeignKey(
        "support.AnonymousProfile",
        on_delete=models.CASCADE,
        related_name="conversations"
    )
    counselor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="counselor_conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.anonymous_profile.anon_id} ↔ {self.counselor.username}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=20)
    text = models.TextField()

    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)