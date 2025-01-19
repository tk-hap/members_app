from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from .models import Exercise, Workout, WorkoutExercise, WorkoutAssignment


class WorkoutExerciseInline(TabularInline):
    model = WorkoutExercise
    extra = 1  # Number of extra forms to display


class WorkoutAssignmentInline(TabularInline):
    model = WorkoutAssignment
    extra = 1  # Number of extra forms to display


class WorkoutAdmin(ModelAdmin):
    inlines = [WorkoutExerciseInline, WorkoutAssignmentInline]
    list_display = ("name", "created_by", "created_at")
    search_fields = ("name", "created_by__username")


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(ModelAdmin):
    list_display = ("workout", "exercise", "sets", "reps", "load", "unit")
    model = WorkoutExercise


@admin.register(Exercise)
class ExerciseAdmin(ModelAdmin):
    list_display = ("name", "description", "youtube_video")
    model = Exercise


@admin.register(WorkoutAssignment)
class WorkoutAssignmentAdmin(ModelAdmin):
    list_display = ("user", "workout", "assigned_at")
    model = WorkoutAssignment


admin.site.register(Workout, WorkoutAdmin)
