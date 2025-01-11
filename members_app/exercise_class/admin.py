from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.contrib.forms.widgets import WysiwygWidget
from .models import ExerciseClassEvent, ExerciseClassOccurrence, Booking

class BookingInline(TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ('participant', 'booking_date',)

class ExerciseClassOccurrenceInline(TabularInline):
    model = ExerciseClassOccurrence
    extra = 1

@admin.register(ExerciseClassEvent)
class ExerciseClassEventAdmin(ModelAdmin):
    inlines = [ExerciseClassOccurrenceInline]
    list_display = ('class_name', 'location', 'trainer')
    search_fields = ('class_name', 'location', 'trainer__first_name', 'trainer__last_name')

@admin.register(ExerciseClassOccurrence)
class ExerciseClassOccurrenceAdmin(ModelAdmin):
    inlines = [BookingInline]
    list_display = ('event', 'scheduled_date')
    search_fields = ('event__class_name', 'scheduled_date')

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('occurrence', 'participant', 'booking_date')
    search_fields = ('occurrence__event__class_name', 'participant__username')
