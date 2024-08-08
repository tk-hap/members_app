from django.urls import path
from dj_rest_auth.views import UserDetailsView


from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("api/user/", UserDetailsView.as_view(), name="rest_user_details"),
]
