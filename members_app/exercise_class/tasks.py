import datetime
from celery import shared_task
from django.utils import timezone
from .models import ExerciseClassEvent, ExerciseClassOccurrence
from .utils import generate_occurrences_for_event


@shared_task
def generate_occurrences():
    events = ExerciseClassEvent.objects.all()
    for event in events:
        generate_occurrences_for_event(event)
