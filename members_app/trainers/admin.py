from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Trainer

@admin.register(Trainer)
class TrainerAdmin(ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "featured",
    ]
    model = Trainer
