from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise, WorkoutAssignment

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1  # Number of extra forms to display

class WorkoutAdmin(admin.ModelAdmin):
    inlines = [WorkoutExerciseInline]
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'created_by__username')

admin.site.register(Exercise)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutAssignment)