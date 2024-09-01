from django.contrib import admin
from .models import Notification
from .forms import SimpleNotificationForm


class SimpleNotificationAdmin(admin.ModelAdmin):
    form = SimpleNotificationForm
    list_display = ["recipient", "level", "description"]

    def save_model(self, request, obj, form, change):
        if not obj.actor:
            obj.actor = request.user  # Automatically set the actor to the current admin
        if not obj.verb:
            obj.verb = "Message"
        super().save_model(request, obj, form, change)


admin.site.unregister(Notification)
admin.site.register(
    Notification, SimpleNotificationAdmin
)  # Register with the custom admin
