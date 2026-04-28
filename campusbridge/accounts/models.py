from symtable import Class

from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES=(('student','Student'),
                  ('staff','Staff'),
                  ('counselor','Counselor'),
                  )
    role=models.CharField(max_length=20, choices=ROLE_CHOICES)