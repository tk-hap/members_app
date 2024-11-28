from django.urls import path

from . import views

urlpatterns = [
    path("upcoming/", views.list_upcoming_classes, name="upcoming-classes"),
    path("home/", views.classes_home, name="classes-home"),
    path("day/", views.list_classes_for_day, name="classes-for-day"),
    path("book/<int:class_id>", views.book_class, name="book"),
    path("book/cancel/<int:class_id>", views.cancel_booking, name="cancel-booking"),
    path(
        "<int:class_id>/",
        views.exercise_class_detail,
        name="exercise-class-detail",
    ),
    path("<int:class_id>/save-to-cal/", views.save_to_calendar, name="save-to-calendar"),
]
