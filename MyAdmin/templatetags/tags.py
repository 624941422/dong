from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_data(*args, **keys):
    return 'tags ok'