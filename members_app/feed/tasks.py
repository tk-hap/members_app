import logging
import requests
from celery import shared_task
from django.utils import timezone
from requests.exceptions import ConnectionError, HTTPError
from exponent_server_sdk import PushClient, PushMessage, PushServerError, DeviceNotRegisteredError, PushTicketError
from exercise_class.models import ExerciseClassOccurrence


logger = logging.getLogger(__name__)

session = requests.Session()
session.headers.update(
    {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)

# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
@shared_task(bind=True, max_retries=3)
def send_push_message_task(self, token, message, extra=None):
    try:
        response = PushClient(session=session).publish(
            PushMessage(
                        to=token,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        logger.error(f"PushServerError: token={token}, message={message}, extra={extra}, errors={exc.errors}, response_data={exc.response_data}")
        raise
    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        logger.error(f"ConnectionError/HTTPError: token={token}, message={message}, extra={extra}")
        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        logger.error(f"PushTicketError: token={token}, message={message}, extra={extra}, details={exc}")

@shared_task
def remind_upcoming_classes():
    now = timezone.now()
    hour_later = now + timezone.timedelta(hours=1)
    upcoming_classes = ExerciseClassOccurrence.objects.filter(reminder_sent="False", scheduled_date__gte=now, scheduled_date__lte=hour_later)

    for exercise_class in upcoming_classes:
        message = f"Reminder: Your class {exercise_class.event.class_name} is starting soon!"
        for participant in exercise_class.get_participants():
            if participant.push_token:
                send_push_message_task.delay(
                    token=participant.push_token,
                    message=message,
                    )
        exercise_class.reminder_sent = True
        exercise_class.save()