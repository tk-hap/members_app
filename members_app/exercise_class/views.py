import datetime
import io
from django.utils import timezone
from django.shortcuts import render
from django.http import FileResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import ExerciseClassOccurrence, ExerciseClassEvent, Booking
from .utils import generate_ics_file, google_calendar_url, outlook_url

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def classes_home(request):
    return render(request, "exercise_class/home.xml")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exercise_class_detail(request, class_id):
    exercise_class = ExerciseClassOccurrence.objects.get(pk=class_id)

    is_available = exercise_class.is_available()
    is_booked = Booking.objects.filter(
        occurrence=exercise_class, participant=request.user
    ).exists()

    start_time = exercise_class.event.start_time
    duration = exercise_class.event.duration
    # Combine the scheduled date and start time to create a datetime object for the event start
    start_datetime = datetime.datetime.combine(exercise_class.scheduled_date, start_time)
    # Calculate the end time by adding the duration to the start time
    end_datetime = start_datetime + duration
    end_time = end_datetime.time()
    time_range = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"



    if is_booked:
        status = "booked"
    elif is_available:
        status = "available"
    else:
        status = "unavailable"

    print(status)

    exercise_class_details = {
        "id": exercise_class.id,
        "class_name": exercise_class.event.class_name,
        "description": exercise_class.event.description,
        "trainer": exercise_class.event.trainer,
        "location": exercise_class.event.location,
        "start_time": exercise_class.event.start_time,
        "end_time": end_time,
        "time_range": time_range,
        "scheduled_date": exercise_class.scheduled_date,
        "duration": exercise_class.event.duration,
    }

    return render(
        request,
        "exercise_class/exercise_class_detail.xml",
        {"class_details": exercise_class_details, "status": status},
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_upcoming_classes(request):
    days_to_load = int(request.GET.get("days", 7))

    start_date = timezone.now().date()

    end_date = start_date + timezone.timedelta(days=days_to_load)

    exercise_classes = (
        ExerciseClassOccurrence.objects.filter(
            scheduled_date__range=[start_date, end_date]
        )
        .select_related("event")
        .order_by("scheduled_date")
    )

    # Group exercise classes by date
    exercise_classes_grouped = {}
    for exercise_class in exercise_classes:
        date = exercise_class.scheduled_date
        if date not in exercise_classes_grouped:
            exercise_classes_grouped[date] = []
        exercise_classes_grouped[date].append(exercise_class)

    return render(
        request,
        "exercise_class/upcoming_list.xml",
        {
            "exercise_classes": exercise_classes_grouped,
        },
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_classes_for_day(request):
    req_date = request.GET.get("date")

    date = timezone.datetime.strptime(req_date, "%Y-%m-%d").date()

    exercise_classes = ExerciseClassOccurrence.objects.filter(
        scheduled_date=date
    ).order_by("scheduled_date")

    return render(
        request,
        "exercise_class/exercise_class_day.xml",
        {
            "exercise_classes": exercise_classes,
            "date": date,
        },
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_class(request, class_id):
    exercise_class = ExerciseClassOccurrence.objects.get(pk=class_id)
    Booking.objects.create(occurrence=exercise_class, participant=request.user)

    return render(request, "exercise_class/cancel.xml", {"class_id": class_id})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, class_id):
    exercise_class = ExerciseClassOccurrence.objects.get(pk=class_id)
    Booking.objects.get(occurrence=exercise_class, participant=request.user).delete()

    return render(request, "exercise_class/book.xml", {"class_id": class_id})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def save_to_calendar(request, class_id):
    """
    Save a class occurrence to a user's calendar.
    Available options are Google Calendar, Outlook and ICS file.
    """

    exercise_class = ExerciseClassOccurrence.objects.get(pk=class_id)

    google = google_calendar_url(exercise_class)
    outlook = outlook_url(exercise_class)

    outlook_mobile = "ms-outlook://events/new?title=MY%20MEETING&startdt=2019-01-29T13:00:00&enddt=2019-01-29T14:00:00&location=LOCATION&attendees=some.person@email.com"

    current_site = get_current_site(request)
    ics_url= f"http://{current_site.domain}{reverse('download-ics', args=[class_id])}"

    return render(request, "exercise_class/add_to_calendar.xml", {"calendar_url": {"google": google, "ics": ics_url, "outlook": outlook}})


@api_view(["GET"])
def download_ics(request, class_id):
    """
    Download an ICS file for a class occurrence.
    """

    exercise_class = ExerciseClassOccurrence.objects.get(pk=class_id)
    ics_file = generate_ics_file(exercise_class)

    return FileResponse(ics_file, content_type='text/calendar', as_attachment=True, filename=f'{exercise_class.event.class_name}.ics') 