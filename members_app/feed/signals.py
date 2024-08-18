from notifications.signals import notify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from exercise_class.models import ExerciseClass


@receiver(pre_delete, sender=ExerciseClass)
def notify_participants(sender, instance, **kwargs):
    notify.send(
        sender=instance,
        recipient=instance.participants.all(),
        verb="Booking",
        description=f"Class {instance.class_name} has been cancelled",
        level="warning"
    )
