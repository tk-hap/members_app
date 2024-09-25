from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #TODO: After configuring django-tenants, this should be set to the tenants timezone
        # https://github.com/django-tenants/django-tenants/issues/18
        timezone.activate('Pacific/Auckland') 
        response = self.get_response(request)
        return response