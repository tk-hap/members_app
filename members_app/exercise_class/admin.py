from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import ExerciseClass


@admin.register(ExerciseClass)
class ExerciseClassAdmin(ModelAdmin):
    list_display = [
        "class_name",
        "scheduled_date",
        "trainer",
        "duration",
        "max_participants",
    ]
    model = ExerciseClass
