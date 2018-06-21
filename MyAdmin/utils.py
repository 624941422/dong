def conditon_filter(request):
    selected = {}
    for k, v in request.GET.items():
        selected[k] = v
    return  selected