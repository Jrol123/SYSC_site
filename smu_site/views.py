from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render


def index(request):
    # template = loader.get_template('organization.html')
    # return HttpResponse(template.render())
    return render(request, 'index.html')
