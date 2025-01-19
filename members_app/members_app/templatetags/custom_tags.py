from django import template
import datetime

register = template.Library()

@register.filter
def humanize_duration(duration):
    """Humanize a timedelta or a DurationField value."""
    if isinstance(duration, datetime.timedelta):
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return f'{hours}h {minutes}m' if hours else f'{minutes}m'

    return duration