from django.shortcuts import render
from .models import Workout, WorkoutExercise
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_workouts(request):
    workouts = Workout.objects.all()
    return render(request, "workouts/workouts_list.xml", {"workouts": workouts})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workout_detail(request, workout_id):
    workout = Workout.objects.get(pk=workout_id)
    workout_exercise = WorkoutExercise.objects.filter(workout=workout_id)
    return render(request, "workouts/workout_detail.xml", {"workout": workout, "exercises": workout_exercise })