from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated 
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import api_view, authentication_classes
from django.utils import timezone
from workouts.models import Workout
from exercise_class.models import Booking, ExerciseClassOccurrence, ExerciseClassEvent


def index(request):
    return render(request, "index.xml", {})

# A view that loads when the React Native app first loads to check if the user is authenticated via the token
# If the user is authenticated, the user is redirected to the home page
# If the user is not authenticated, the user is redirected to the login page
def check_auth(request):
    if request.user:
        return render(request, "home.xml", {})


@api_view(["GET"])
@authentication_classes([])
def home(request):
    user = None
    try:
       auth_result = TokenAuthentication().authenticate(request)
       if auth_result is not None:
           user = auth_result[0]
    except AuthenticationFailed:
        return render(request, "authentication/login.xml", {})

    if user:
        # Get user's upcoming classes
        upcoming_classes = ExerciseClassOccurrence.objects.filter(
            scheduled_date__gte=timezone.now().date(),
            booking__participant=user,
        )

        # Get featured workouts
        featured_workouts = Workout.objects.filter(featured=True)

        return render(request, "home.xml", { "featured_workouts": featured_workouts, "class_bookings": upcoming_classes })
    else:
        return render(request, "authentication/login.xml", {})