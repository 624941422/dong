from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_data(obj, field):
    try:
        field_val = getattr(obj, field)
        field_obj = obj._meta.get_field(field)
        if field_obj.choices:
            field_val = getattr(obj, "get_%s_display" % field)()
    except Exception as e:
        if 'object has no attribute' in str(e):
            return '<a href=''>%s<a>' % (obj,)
    return field_val