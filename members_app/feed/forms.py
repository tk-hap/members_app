from django import forms
from django.contrib.auth.models import Group
from users.models import User
from .models import Notification
from notifications.signals import notify

class SimpleNotificationForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,  # Make the recipient field optional
        label="Recipient",
        help_text="Select an individual user to receive the notification."
    )
    recipient_group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Recipient Group",
        help_text="Select a group to notify all its members."
    )

    class Meta:
        model = Notification
        fields = ['recipient', 'recipient_group', 'level', 'description']


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['recipient_group']:
            group = self.cleaned_data['recipient_group']
            notify.send(
                sender=self.instance,
                recipient=group,
                verb=instance.verb,
                description=instance.description,
                level=instance.level,
                target=instance.target,
                action_object=instance.action_object,
            )
        if commit:
            instance.save()
            self.save_m2m()
        return instance