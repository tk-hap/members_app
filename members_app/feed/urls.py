from django.urls import path

from . import views

urlpatterns = [
    path("", views.feed_home, name="feed-home"),
    path("<int:page>", views.feed_page, name="feed-page"),
]
