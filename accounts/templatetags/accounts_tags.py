import datetime
from django import template

register = template.Library()

@register.simple_tag
def is_instructor(user):
    return user.role==2