from django.db import models

# Create your models here.
from support.models import AnonymousProfile
from accounts.models import User
class Conversation(models.Model):
    anonymous_profile=models.ForeignKey(AnonymousProfile,on_delete=models.CASCADE)
    counselor=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('anonymous_profile', 'counselor')





class Message(models.Model):
        SENDER_TYPE=[('student','Student'),
                     ('counselor','Counselor')
                     ]

        conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE)
        sender_type=models.CharField(max_length=20,choices=SENDER_TYPE)
        text=models.TextField()
        timestamp=models.DateTimeField(auto_now_add=True)

