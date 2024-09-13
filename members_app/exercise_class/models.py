import datetime
from django.db import models
from django.utils import timezone
from users.models import User
from trainers.models import Trainer


class ExerciseClass(models.Model):
    class_name = models.CharField(max_length=50)
    scheduled_date = models.DateTimeField()
    participants = models.ManyToManyField(User)
    max_participants = models.IntegerField(null=True)
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.SET_NULL)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.class_name

    def is_available(self):
        if self.participants.count() >= self.max_participants:
            return False
        else:
            return True
    
    def is_upcoming(self):
        if self.scheduled_date > timezone.now():
            return True
        else:
            return False