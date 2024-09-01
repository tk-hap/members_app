from django.urls import path

from . import views

urlpatterns = [
    path("push-token/", views.save_push_token, name="save-push-token"),
]