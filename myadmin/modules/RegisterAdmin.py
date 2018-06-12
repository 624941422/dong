from app01 import models

register_dic = {}

class MyAdmin(object):
    list_display = ()

class CustomerAdmin(MyAdmin):
    list_display = ('id', 'qq', 'source', 'consultant', 'date')

def register(models_class, admin_class=None):
    app_name = models_class._meta.app_label
    if app_name not in register_dic:
        register_dic[app_name] = {}
    register_dic[app_name][models_class._meta.object_name] = admin_class
register(models.Customer, CustomerAdmin)
register(models.UserProfile)