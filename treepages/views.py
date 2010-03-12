from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.http import Http404

from treepages.models import Page


def base_url_page_handler(request, path=None):
    if path == None or path == '':
        raise Http404
    else:
        page = Page.objects.page_for_path_or_404(path)
        return render_to_response(
            'treepages/pages/base.html',
            {'page':page},
            context_instance=RequestContext(request)
            )

