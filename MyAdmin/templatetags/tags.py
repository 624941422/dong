from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_data(obj, field):
    try:
        field_val = getattr(obj, field)
        field_obj = obj._meta.get_field(field)
        if field_obj.choices:
            # field_val = obj.get_source_display()
            field_val = getattr(obj, 'get_%s_display' % field)()
        if type(field_val).__name__ == 'datetime':
            field_val = field_val.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        if 'object has no attribute' in str(e):
            return mark_safe('<a href=''>%s<a>' % (obj,))
    return field_val

@register.simple_tag
def render_filter(condtion, model, mychoices):
    selected = ''
    html = '''<select class="form-control" style="height: 30px;font-size:12px" name="%s"><option value=""> --- </option> ''' % condtion
    field_obj = model._meta.get_field(condtion)
    if field_obj.choices:
        for item in field_obj.choices:
            if mychoices:
                if mychoices[condtion] == str(item[0]):
                    selected = 'selected'
            html += '''<option value="%s" %s> %s </option>''' % (item[0], selected, item[1])
            selected = ''
    elif type(field_obj).__name__ == 'ForeignKey':
        for item in field_obj.get_choices(include_blank=False):
            if mychoices:
                if mychoices[condtion] == str(item[0]):
                    selected = 'selected'
            html += '''<option value="%s" %s> %s </option>''' % (item[0], selected, item[1])
            selected = ''
    html += '''</select>'''
    return html