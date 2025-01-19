from django.db import models
from django.utils import timezone
from notifications.base.models import AbstractNotification

class Notification(AbstractNotification):

    push_notification = models.BooleanField(default=False)

    def time_since(self):
        today = timezone.now().day
        delta = today - self.timestamp.day
        if self.timestamp.day == today:
            return self.timestamp.time()
        elif delta == 1:
            return "yesterday"
        else:
            return f"{delta} days ago"

    class Meta(AbstractNotification.Meta):
        abstract = False

