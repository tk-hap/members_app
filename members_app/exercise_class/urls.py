from django.urls import path

from . import views

urlpatterns = [
    path("", views.exercise_class_all, name="exercise-class-all"),
    path("book/<int:class_id>", views.book_class, name="book"),
    path("book/cancel/<int:class_id>", views.cancel_booking, name="cancel-booking"),
    path(
        "<int:class_id>/",
        views.exercise_class_detail,
        name="exercise-class-detail",
    ),
]
