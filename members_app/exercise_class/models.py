import datetime

from django.db import models
from django.utils import timezone


class Member(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Trainer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=50)
    user_avatar = models.ImageField(upload_to="media/")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ExerciseClass(models.Model):
    class_name = models.CharField(max_length=50)
    scheduled_date = models.DateTimeField()
    participants = models.ManyToManyField(Member)
    max_participants = models.IntegerField(null=True)
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.class_name

    def due_soon(self):
        return self.scheduled_date <= timezone.now() - datetime.timedelta(days=2)
