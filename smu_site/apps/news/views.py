from django.shortcuts import render, loader
from django.http import HttpResponse
from .models import Image


def index(request):
    return render(request, 'news/index.html')
