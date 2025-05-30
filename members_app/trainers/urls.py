from django.urls import path

from . import views

urlpatterns = [
    path("", views.trainer_home, name="trainer-home"),
    path("list", views.trainer_list, name="trainer-list"),
    path("<int:trainer_id>", views.trainer, name="trainer"),
    path("full-bio/<int:trainer_id>", views.trainer_full_bio, name="trainer-full-bio"),
]
