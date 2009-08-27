from django.http import Http404

def base_url_page_handler(request, path=None):
    if path == None or path == '':
        homepage(request)
    else:
        raise Http404 

def homepage(request):
    raise Http404 
