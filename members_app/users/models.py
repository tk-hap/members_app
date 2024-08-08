from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import zoneinfo

TIMEZONES = tuple(zip(
    zoneinfo.available_timezones(),
    zoneinfo.available_timezones()
))

class User(AbstractUser):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)


class UserProfile(models.Model):
    models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='NZST')