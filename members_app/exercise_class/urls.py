from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_upcoming_classes, name="upcoming-classes"),
    path("day/", views.list_classes_for_day, name="classes-for-day"),
    path("book/<int:class_id>", views.book_class, name="book"),
    path("book/cancel/<int:class_id>", views.cancel_booking, name="cancel-booking"),
    path(
        "<int:class_id>/",
        views.exercise_class_detail,
        name="exercise-class-detail",
    ),
]
