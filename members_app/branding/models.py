from django.db import models

class Branding(models.Model):
    logo = models.ImageField(upload_to="branding/logos/")
    primary_color = models.CharField(null=True, blank=True, default="#6750A4", max_length=255)
    secondary_color= models.CharField(null=True, blank=True, default="#E8DEF8", max_length=255)

    def __str__(self):
        return "Global Branding Settings"
    
    def save(self, *args, **kwargs):
        if not self.pk and Branding.objects.exists():
            raise ValueError("There can only be one Branding instance")
        super().save(*args, **kwargs)