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
def render_filter_ele(condtion, instance_model, filter_condtions):
    print(instance_model)
    select_ele = '''<select class="form-control" name='%s' ><option value=''>----</option>''' %condtion

    field_obj = instance_model._meta.get_field(condtion)
    if field_obj.choices:
        selected = ''
        for choice_item in field_obj.choices:
            print("choice",choice_item,filter_condtions.get(condtion),type(filter_condtions.get(condtion)))
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected ="selected"

            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected =''

    if type(field_obj).__name__ == "ForeignKey":
        selected = ''
        for choice_item in field_obj.get_choices()[1:]:
            if filter_condtions.get(condtion) == str(choice_item[0]):
                selected = "selected"
            select_ele += '''<option value='%s' %s>%s</option>''' %(choice_item[0],selected,choice_item[1])
            selected = ''
    select_ele += "</select>"
    return mark_safe(select_ele)