"""
URL configuration for members_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import notifications.urls

from . import views

urlpatterns = [
    path("health", views.health_check, name="health_check"),
    path("admin/", admin.site.urls),
    path("auth/", include("authentication.urls")),
    path("classes/", include("exercise_class.urls")),
    path("users/", include("users.urls")),
    path("feed/", include("feed.urls")),
    path("trainers/", include("trainers.urls")),
    path("workouts/", include("workouts.urls")),
    path("home/", views.home, name="home"),
    path("index.xml", views.index, name="index"),
    path(
        "inbox/notifications/", include(notifications.urls, namespace="notifications")
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)