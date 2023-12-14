from django.shortcuts import render
from info.models import Institute, Scientist, Grant


def institutes(request):
    inst = Institute.objects.all().order_by('name')
    return render(request, 'info/institutes.html',
                  {'institutes': inst})


def grant(request):
    grants = (Grant.objects.filter(queue_id__isnull=True)
              .order_by("end_doc_date"))
    
    return render(request, 'info/grant.html',
                  {'grants': grants})


def organization(request):
    return render(request, 'info/organization.html')
    
    
def institute_info(request):
    return render(request, 'info/institute_info.html')
