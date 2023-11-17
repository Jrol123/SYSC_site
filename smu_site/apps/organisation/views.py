from django.shortcuts import render, loader
from django.http import HttpResponse


def index(request):
    # template = loader.get_template('index.html')
    # return HttpResponse(template.render())
    return render(request, 'organisation/index.html')
