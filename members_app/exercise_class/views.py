import datetime
from django.shortcuts import render
from django.http import HttpResponse

from .models import ExerciseClass


# Just for testing
def index(request):
    return render(request, "exercise_class/index.xml")


def exercise_class_detail(request, class_id):
    exercise_class_details = ExerciseClass.objects.get(pk=class_id)
    context = {"class_details": exercise_class_details}
    return render(request, "exercise_class/exercise_class_detail.xml", context)


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
