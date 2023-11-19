from django.shortcuts import render


def institutes(request):
    return render(request, 'info/institutes.html')


def grant(request):
    return render(request, 'info/grant.html')


def organisation(request):
    return render(request, 'info/organisation.html')
