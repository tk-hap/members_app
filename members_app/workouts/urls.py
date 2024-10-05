from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_workouts, name="workouts-home"),
    path("<int:workout_id>/", views.workout_detail, name="workout-detail"),
    path("exercise/<int:workout_exercise_id>/", views.exercise_detail, name="exercise-detail"),
]
