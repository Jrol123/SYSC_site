from django.shortcuts import render, loader
from django.http import HttpResponse


def index(request):
    return render(request, 'news/index.html')
