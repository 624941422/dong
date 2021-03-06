from django.shortcuts import render
from MyAdmin.modules import RegisterAdmin
import importlib
from MyAdmin.utils import conditon_filter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    selected_filter = dict(filter(lambda x: x[1] != '' and x[0] != 'page' and x[0] != 'o', selected.items()))
    if selected_filter:
        queryset = model_obj.objects.filter(**selected_filter).order_by("%s" % request.GET.get('o') if\
    request.GET.get('o') else '-id')
    else:
        queryset = model_obj.objects.all().order_by("%s" % request.GET.get('o') if request.GET.get('o') else '-id')

    try:
        per_page = admin_class.list_per_page
    except AttributeError:
        per_page = 20

    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    data = {'app': app,
            'model': model,
            'display': display,
            'admin_class': admin_class,
            'model_obj': model_obj,
            'selected': selected,
            'contacts': contacts
            }
    return render(request, 'my_admin/table_object.html', {'data': data})