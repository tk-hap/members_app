from django import forms
from .models import Notification

class SimpleNotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['recipient', 'level', 'description']