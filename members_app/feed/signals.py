from notifications.signals import notify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from exercise_class.models import ExerciseClassOccurrence
from .tasks import send_push_message_task


@receiver(pre_delete, sender=ExerciseClassOccurrence)
def notify_participants(sender, instance, **kwargs):
    if not instance.is_upcoming():
        return

    message = f"{instance.event.class_name} class on {instance.scheduled_date.strftime('%b %d')} has been cancelled"

    participants = instance.get_participants()

    for participant in participants:
        send_push_message_task.delay(
            token=participant.push_token,
            message=message,
        )

    notify.send(
        sender=instance,
        recipient=participants,
        verb="Booking",
        description=message,
        level="warning",
    )
