import zoneinfo

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        def _activate_tz(tz):
            timezone.activate(zoneinfo.ZoneInfo(tz))
            
        tzname = request.session.get("django_timezone", None)

        if tzname:
            _activate_tz(tzname)
        else:
            # no time zone stored in session cookie, check to see if available from user profile
            user = request.user
            if hasattr(user, 'user_profile'):
                tzname = user.user_profile.timezone
                # set the cookie
                request.session['django_timezone'] = tzname
                _activate_tz(tzname)
            else:
                timezone.deactivate()
        return self.get_response(request)