from django.shortcuts import render


def institutes(request):
    return render(request, 'info/institutes.html')


def grant(request):
    return render(request, 'info/grant.html')


def documents(request):
    return render(request, 'info/documents.html')
