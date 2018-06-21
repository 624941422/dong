from django.shortcuts import render
from MyAdmin.modules import RegisterAdmin
import importlib
from MyAdmin.utils import conditon_filter

dic = RegisterAdmin.register_dic

def index(request):
    return render(request, 'my_admin/index.html', {"dic_value": dic})

def table_object(request, app, model):
    selected = conditon_filter(request)
    display = []
    admin_class = dic[app][model]
    try:
        display = admin_class.list_display
    except Exception as e:
        if 'list_display' in str(e):
            display = [model]
    models = importlib.import_module('%s.models' % app)
    model_obj = getattr(models, model)
    queryset = model_obj.objects.all()
    data = {'app': app,
            'model': model,
            'display': display,
            'queryset': queryset,
            'admin_class': admin_class,
            'model_obj': model_obj,
            'selected': selected,
            }
    return render(request, 'my_admin/table_object.html', {'data': data})