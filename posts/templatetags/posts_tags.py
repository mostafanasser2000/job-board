from django import template
from django.utils import timezone

register = template.Library()

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = SECONDS_IN_MINUTE * 60
SECONDS_IN_DAY = SECONDS_IN_HOUR * 24
SECONDS_IN_WEEK = SECONDS_IN_DAY * 7
SECONDS_IN_MONTH = SECONDS_IN_DAY * 30
SECONDS_IN_YEAR = SECONDS_IN_DAY * 365


@register.filter(expects_localtime=True)
def transform_date(value):
    if not value:
        return ""
    try:
        diff = timezone.now() - value
        total_seconds = diff.total_seconds()
        if total_seconds >= SECONDS_IN_YEAR:
            years = total_seconds // SECONDS_IN_YEAR
            return f"{int(years)} years ago"
        if total_seconds >= SECONDS_IN_MONTH:
            months = total_seconds // SECONDS_IN_MONTH
            return f"{int(months)} months ago"
        if total_seconds >= SECONDS_IN_WEEK:
            weeks = total_seconds // SECONDS_IN_WEEK
            return f"{int(weeks)} weeks ago"
        if total_seconds >= SECONDS_IN_DAY:
            days = total_seconds // SECONDS_IN_DAY
            return f"{int(days)} days ago"
        if total_seconds >= SECONDS_IN_HOUR:
            hours = total_seconds // SECONDS_IN_HOUR
            return f"{int(hours)} hours ago"
        if total_seconds >= SECONDS_IN_MINUTE:
            minutes = total_seconds // SECONDS_IN_MINUTE
            return f"{int(minutes)} minutes ago"
        return f"{int(total_seconds)} seconds ago"
    except (AttributeError, TypeError):
        return ""
