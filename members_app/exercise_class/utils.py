#from django.utils import timezone
import datetime

MAX_DAYS_AHEAD = 14  # Maximum number of days ahead to generate occurrences

def generate_occurrences_for_event(event):
    from .models import ExerciseClassOccurrence # Local import to avoid circular imports
    now = datetime.datetime.now()
    end_date = now + datetime.timedelta(days=MAX_DAYS_AHEAD)
    print(now)
    print(end_date)
    if event.schedule:
        occurrences = event.schedule.between(now, end_date, inc=True)
        for occurrence_date in occurrences:
            ExerciseClassOccurrence.objects.get_or_create(
                event=event,
                scheduled_date=occurrence_date.date(),
                #defaults={'duration': event.duration}
            )