from django.db import models
from users.models import User


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    youtube_video = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Workout(models.Model):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"

    DIFFICULTY_CHOICES = [
        (BEGINNER, "Beginner"),
        (INTERMEDIATE, "Intermediate"),
        (ADVANCED, "Advanced"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default=BEGINNER
    )
    duration = models.DurationField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    KG = "kg"
    LBS = "lbs"
    PERCENT = "%"

    LOAD_CHOICES = [
        (KG, "Kilograms"),
        (LBS, "Pounds"),
        (PERCENT, "%"),
    ]

    workout = models.ForeignKey(
        Workout, related_name="workout_exercises", on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    load = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=5, choices=LOAD_CHOICES, default=KG, blank=True, null=True)

    def __str__(self):
        return f"{self.workout.name} - {self.exercise.name}"


class WorkoutAssignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name}"
