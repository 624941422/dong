from django.shortcuts import render

def index(request):
    return render(request, 'bootstrap-index.html')

def customer_list(request):
    return render(request, 'sale/customer-index.html')