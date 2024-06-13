from django import template
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def format_datetime(value):
    adjusted_time = value - timedelta(hours=3)
    return adjusted_time.strftime('%d/%m/%Y %H:%M')