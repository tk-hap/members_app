from notifications.signals import notify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from exercise_class.models import ExerciseClass
from .tasks import send_push_message_task


@receiver(pre_delete, sender=ExerciseClass)
def notify_participants(sender, instance, **kwargs):
    message = f"Class {instance.class_name} has been cancelled"

    for participant in instance.participants.all():
        send_push_message_task(
            token=participant.push_token,
            message=message,
        )

    notify.send(
        sender=instance,
        recipient=instance.participants.all(),
        verb="Booking",
        description=message,
        level="warning"
    )
