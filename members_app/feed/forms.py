from django import forms
from django.contrib.auth.models import Group
from users.models import User
from .models import Notification
from notifications.signals import notify
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldBooleanSwitchWidget, UnfoldAdminTextareaWidget


class SimpleNotificationForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,  # Make the recipient field optional
        label="Recipient",
        help_text="Select an individual user to receive the notification.",
        widget=UnfoldAdminSelectWidget
    )
    recipient_group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Recipient Group",
        help_text="Select a group to notify all its members.",
        widget=UnfoldAdminSelectWidget
    )

    description = forms.CharField(
        required=True,
        label="Message",
        help_text="Enter the message to be sent in the notification.",
        widget=UnfoldAdminTextareaWidget
    )

    push_notification = forms.BooleanField(
        required=False,
        label="Send Push Notification",
        help_text="Send a push notification to the recipient(s) device.",
        widget=UnfoldBooleanSwitchWidget
    )


    class Meta:
        model = Notification
        fields = ['recipient', 'recipient_group', 'description']


    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data['recipient_group']:
            group = self.cleaned_data['recipient_group']
            notify.send(
                sender=self.instance,
                recipient=group,
                verb=instance.verb,
                description=instance.description,
                level="info",
                target=instance.target,
                action_object=instance.action_object,
            )
        if commit:
            instance.save()
            self.save_m2m()
        return instance