from datetime import datetime
from datetime import timedelta
from django import template

register = template.Library()

@register.filter
def count_duration(end: datetime, start: datetime) -> str:
    delta = end - start
    seconds = delta.seconds

    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    result = ""

    if hours:
        result += f"{hours} часов, "
    
    if minutes:
        result += f"{minutes} минут, "
    
    result += f"{seconds} секунд"
    
    return result