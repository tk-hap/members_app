from django.shortcuts import render
from .models import Workout, WorkoutExercise
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workouts_home(request):
    """
    Home page for workouts.
    """
    workouts = Workout.objects.all()
    return render(request, "workouts/workouts_home.xml", {"workouts": workouts})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_all_workouts(request):
    """
    List all workouts.
    """
    workouts = Workout.objects.all()
    return render(request, "workouts/workouts_list.xml", {"workouts": workouts})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_assigned_workouts(request):
    """
    List all workouts assigned to the current user.
    """

    workouts = Workout.objects.filter(workoutassignment__user=request.user)
    return render(request, "workouts/workouts_list.xml", {"workouts": workouts})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def workout_detail(request, workout_id):
    """
    Display details for a specific workout.
    Includes a list of exercises in the workout.
    """

    workout = Workout.objects.get(pk=workout_id)
    workout_exercise = WorkoutExercise.objects.filter(workout=workout_id)
    return render(
        request,
        "workouts/workout_detail.xml",
        {"workout": workout, "exercises": workout_exercise},
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exercise_detail(request, workout_exercise_id):
    """
    Display details for a specific exercise.
    """

    workout_exercise = WorkoutExercise.objects.get(pk=workout_exercise_id)
    return render(
        request, "workouts/exercise_detail.xml", {"workout_exercise": workout_exercise}
    )
