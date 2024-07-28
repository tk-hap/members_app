from django.urls import path

from . import views

urlpatterns = [
    path("", views.exercise_class_all, name="exercise-class-all"),
    path(
        "<int:class_id>/",
        views.exercise_class_detail,
        name="exercise-class-detail",
    ),
]
