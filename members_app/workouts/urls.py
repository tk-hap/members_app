from django.urls import path

from . import views

urlpatterns = [
    path("", views.workouts_home, name="workouts-home"),
    path("all/", views.list_all_workouts, name="all-workouts-list"),
    path("assigned/", views.list_assigned_workouts, name="assigned-workouts-list"),
    path("<int:workout_id>/", views.workout_detail, name="workout-detail"),
    path("exercise/<int:workout_exercise_id>/", views.exercise_detail, name="exercise-detail"),
    path("exercise/<int:workout_id>/save/", views.save_workout , name="save-workout"),
    path("exercise/<int:workout_id>/unsave/", views.unsave_workout, name="unsave-workout"),
]
