from django.db import models
from django.utils import timezone
from users.models import User
from trainers.models import Trainer
from recurrence.fields import RecurrenceField
from .utils import generate_occurrences_for_event


class ExerciseClassEvent(models.Model):
    class_name = models.CharField(max_length=50)
    description = models.TextField()
    location = models.CharField(max_length=50)
    max_participants = models.IntegerField(null=True)
    trainer = models.ForeignKey(Trainer, null=True, on_delete=models.SET_NULL)
    start_time = models.TimeField()
    duration = models.DurationField()
    schedule = RecurrenceField()  # Recurrence field for scheduling

    def __str__(self):
        return self.class_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Generate occurrences for the event after saving
        generate_occurrences_for_event(self)


class ExerciseClassOccurrence(models.Model):
    event = models.ForeignKey(
        ExerciseClassEvent, related_name="occurrences", on_delete=models.CASCADE
    )
    scheduled_date = models.DateField()
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.event.class_name} on {self.scheduled_date}"

    def get_participants(self):
        return User.objects.filter(booking__occurrence=self)

    def is_upcoming(self):
        return self.scheduled_date > timezone.now().date()

    def is_available(self):
        return self.get_participants().count() < self.event.max_participants


class Booking(models.Model):
    occurrence = models.ForeignKey(ExerciseClassOccurrence, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "occurrence",
            "participant",
        )  # Avoid duplicate bookings for the same occurrence

    def __str__(self):
        return f"{self.participant.username} booked for {self.occurrence}"
