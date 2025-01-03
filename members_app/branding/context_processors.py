from .models import Branding
from django.urls import reverse

def branding(request):
    if request.path.startswith(reverse('admin:index')):
        return {}
    try:
        branding = Branding.objects.first()
    except Branding.DoesNotExist:
        branding = None
    return {'branding': branding}