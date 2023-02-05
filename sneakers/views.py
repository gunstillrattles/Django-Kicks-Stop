from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import render

def index(request):
    return HttpResponse("KicksStop")

def sneaker(request, sneakerid):
    return HttpResponse(f"View of Sneaker {sneakerid}")

def sneakers(request):
    return HttpResponse("<h1>Sneakers page</h1>")

def pageNotFound(request, exception):
    template = loader.get_template('404.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponseNotFound(rendered_page)

def pageBadRequest(request, exception):
    template = loader.get_template('400.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponseBadRequest(rendered_page)

def pageForbidden(request, exception):
    template = loader.get_template('403.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponseForbidden(rendered_page)