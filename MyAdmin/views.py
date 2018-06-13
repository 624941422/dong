from django.shortcuts import render
from MyAdmin.modules import RegisterAdmin

def index(request):
    dic = RegisterAdmin.register_dic
    return render(request, 'my_admin/index.html', {"dic_value": dic})

def table_object(request, app, model):
    data = {'app': app, 'model': model}
    return render(request, 'my_admin/table_object.html', {'data': data})