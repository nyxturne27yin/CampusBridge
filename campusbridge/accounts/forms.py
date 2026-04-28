

from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=User
        fields=['username','email','role','password']

    def clean_email(self):
            email = self.cleaned_data.get('email')
            if not email.endswith('@uap-bd.edu'):
                raise forms.ValidationError("Use UAP email")
                return email

