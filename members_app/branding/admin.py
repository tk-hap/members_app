from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldAdminColorInputWidget
from django.db import models
from django.utils.html import format_html

from .models import Branding

@admin.register(Branding)
class BrandingAdmin(ModelAdmin):
    model = Branding

    formfield_overrides = {
        models.CharField: {"widget": UnfoldAdminColorInputWidget},
    }

    def has_add_permission(self, request):
        # Only allow one instance of Branding
        return not Branding.objects.exists()