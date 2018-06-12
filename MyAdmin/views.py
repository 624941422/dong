from django.shortcuts import render
from MyAdmin.modules import RegisterAdmin

def index(request):
    dic = RegisterAdmin.register_dic
    return render(request, 'my_admin/index.html', {"dic_value": dic})