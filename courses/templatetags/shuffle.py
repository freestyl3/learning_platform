import random
from django import template
register = template.Library()

@register.filter
def shuffle(arg):
    tmp = list(arg)
    while tmp == list(arg):
        random.shuffle(tmp)
    return tmp