import datetime
from django.shortcuts import render
from django.template.response import TemplateResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import ExerciseClass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exercise_class_detail(request, class_id):
    exercise_class_details = ExerciseClass.objects.get(pk=class_id)
    context = {
        "class_details": exercise_class_details,
        "available": exercise_class_details.is_available(),
        "booked": exercise_class_details.participants.filter(
            id=request.user.id
        ).exists(),
    }
    return render(request, "exercise_class/exercise_class_detail.xml", context)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exercise_class_all(request):
    req_date = request.GET.get("date")

    if req_date:
        date = datetime.datetime.strptime(req_date, "%Y-%m-%d").date()
    else:
        date = datetime.date.today()

    exercise_classes = ExerciseClass.objects.filter(scheduled_date__date=date)

    context = {
        "exercise_classes": exercise_classes,
        "date": date,
    }
    return render(request, "exercise_class/exercise_class_all.xml", context)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_class(request, class_id):
    exercise_class_details = ExerciseClass.objects.get(pk=class_id)
    exercise_class_details.participants.add(request.user)
    return render(request, "exercise_class/cancel.xml", {"class_id": class_id})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, class_id):
    exercise_class_details = ExerciseClass.objects.get(pk=class_id)
    exercise_class_details.participants.remove(request.user)
    return render(request, "exercise_class/book.xml", {"class_id": class_id})
