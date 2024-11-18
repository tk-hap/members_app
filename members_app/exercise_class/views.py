import datetime
from django.utils import timezone
from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import ExerciseClassOccurrence, ExerciseClassEvent, Booking


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exercise_class_detail(request, class_id):
    exercise_class = ExerciseClassOccurrence.objects.get(pk=class_id)

    is_available = exercise_class.is_available()
    is_booked = Booking.objects.filter(
        occurrence=exercise_class, participant=request.user
    ).exists()

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
        "exercise_class/exercise_class_upcoming.xml",
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
