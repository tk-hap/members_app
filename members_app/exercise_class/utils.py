from django.utils import timezone
from io import BytesIO
from datetime import datetime, timedelta
from ics import Calendar, Event
from urllib.parse import urlencode

def generate_occurrences_for_event(event):
    """
    Generate occurrences for an event based on its schedule.
    """

    from .models import ExerciseClassOccurrence # Local import to avoid circular imports
    MAX_DAYS_AHEAD = 14  # Maximum number of days ahead to generate occurrences

    now = datetime.now()
    end_date = now + timedelta(days=MAX_DAYS_AHEAD)
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

    # Combine the scheduled_date and start_time to create a datetime object for the event start
    start_datetime = datetime.combine(occurrence.scheduled_date, occurrence.event.start_time)

    if timezone.is_naive(start_datetime):
        start_datetime = timezone.make_aware(start_datetime, timezone.get_current_timezone())

    e.begin = start_datetime

    # Set the duration of the event
    e.duration = occurrence.event.duration
    e.created = datetime.now()

    c.events.add(e)

    ics_content = c.serialize()
    ics_file = BytesIO(ics_content.encode('utf-8'))
    return ics_file


def stringify(input_dict):
    return urlencode({k: v for k, v in sorted(input_dict.items()) if v is not None})

def google_calendar_url(occurrence):
    """
    Generate a Google Calendar link for an event.
    """

    base_url = "https://www.google.com/calendar/render"

    start_datetime = datetime.combine(occurrence.scheduled_date, occurrence.event.start_time)
    end_datetime = start_datetime + occurrence.event.duration

    details = {
        "action": "TEMPLATE",
        "text": occurrence.event.class_name,
        "dates": f'{start_datetime.strftime("%Y%m%dT%H%M%S")}/{end_datetime.strftime("%Y%m%dT%H%M%S")}',
        "details": occurrence.event.description,
        "location": occurrence.event.location,
    }

    return f"{base_url}?{stringify(details)}"

def outlook_url(occurrence):
    """
    Generate an Outlook Calendar link for an event.
    """

    base_url = "https://outlook.live.com/calendar/0/deeplink/compose?"

    start_datetime = datetime.combine(occurrence.scheduled_date, occurrence.event.start_time)
    end_datetime = start_datetime + occurrence.event.duration

    details = {
        "path":  "/calendar/action/compose",
        "subject": occurrence.event.class_name,
        "startdt": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "enddt": end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "body": occurrence.event.description,
        "location": occurrence.event.location,
    }

    return f"{base_url}{stringify(details)}"

def outlook_mobile_url(occurrence):
    """
    Generate an Outlook Mobile Calendar link for an event.
    """

    # CURRENTLY NOT WORKING: Can't pass the date and time
    base_url = "ms-outlook://events/new?"


    start_datetime = datetime.combine(occurrence.scheduled_date, occurrence.event.start_time)
    end_datetime = start_datetime + occurrence.event.duration


    details = {
        "title": occurrence.event.class_name,
        "start": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "end": end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
        "description": occurrence.event.description,
        "location": occurrence.event.location,
    }

    print(f'Outlook {details["start"]}')

    return f"{base_url}{stringify(details)}"
