from django.db import models
from accounts.models import User
from support.models import AnonymousProfile

class CounselorAvailability(models.Model):
    counselor=models.ForeignKey(User,on_delete=models.CASCADE)

    date=models.DateField()
    time_slot=models.TimeField()
    is_booked=models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'time_slot']

    def __str__(self):
        return f"{self.counselor.username}-{self.date} {self.time_slot}"



class Appointment(models.Model):
    STATUS_CHOICE=[('pending','Pending'),
                   ('rejected','Rejected'),
                   ('approved','Approved')]

    anonymous_profile=models.ForeignKey(AnonymousProfile,on_delete=models.CASCADE)
    counselor = models.ForeignKey(User, on_delete=models.CASCADE)
    slot=models.ForeignKey(CounselorAvailability,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=STATUS_CHOICE,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.anonymous_profile} → {self.counselor} ({self.status})"




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
