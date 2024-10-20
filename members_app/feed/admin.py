from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Notification
from .forms import SimpleNotificationForm


admin.site.unregister(Notification)

@admin.register(Notification)
class SimpleNotificationAdmin(ModelAdmin):
    form = SimpleNotificationForm
    list_display = ["recipient", "level", "description"]

    def save_model(self, request, obj, form, change):
        if not obj.actor:
            obj.actor = request.user  # Automatically set the actor to the current admin
        if not obj.verb:
            obj.verb = "Message"
        super().save_model(request, obj, form, change)
