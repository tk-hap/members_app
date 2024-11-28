from django.core.files.base import ContentFile
from io import BytesIO
import datetime
from ics import Calendar, Event


def generate_occurrences_for_event(event):
    """
    Generate occurrences for an event based on its schedule.
    """

    from .models import ExerciseClassOccurrence # Local import to avoid circular imports
    MAX_DAYS_AHEAD = 14  # Maximum number of days ahead to generate occurrences

    now = datetime.datetime.now()
    end_date = now + datetime.timedelta(days=MAX_DAYS_AHEAD)
    if event.schedule:
        occurrences = event.schedule.between(now, end_date, inc=True)
        for occurrence_date in occurrences:
            ExerciseClassOccurrence.objects.get_or_create(
                event=event,
                scheduled_date=occurrence_date.date(),
                #defaults={'duration': event.duration}
            )


def generate_ics_file(occurrence):
    """
    Generate an ICS file for an occurrence.
    """

    c = Calendar()
    e = Event()
    e.name = occurrence.event.class_name
    e.description = occurrence.event.description
    e.location = occurrence.event.location
    e.begin = occurrence.scheduled_date
    e.duration = occurrence.event.duration
    c.events.add(e)

    ics_content = c.serialize()
    ics_file = BytesIO(ics_content.encode('utf-8'))
    return ics_file