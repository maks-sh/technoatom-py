# from django.shortcuts import render
# from django.template import RequestContext, loader
# from django.http import HttpResponse
from django.shortcuts import render_to_response
# Create your views here.


def index(request):
    response = render_to_response('index.html', {})
    return response


def charges(request):
    response = render_to_response('charges.html', {})
    return response

    # template = loader.get_template('charges.html')
    # context = RequestContext(request, {
    #
    # })
    # return HttpResponse(template.render(context))