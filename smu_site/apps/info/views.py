from django.shortcuts import render, Http404
from info.models import Institute, Scientist, Grant
from news.models import Image


def institutes(request):
    inst = Institute.objects.all().order_by('name')
    return render(request, 'info/institutes.html',
                  {'institutes': inst})


def grant(request):
    grants = (Grant.objects.filter(queue_id__isnull=True)
              .order_by('end_doc_date'))
    grants = [(g, Image.objects.filter(grant_id=g.id)
               .order_by('id').first())
              for g in grants]
    return render(request, 'info/grant.html',
                  {'grants': grants})


def organization(request):
    return render(request, 'info/organization.html')
    
    
def institute_info(request, inst_id):
    try:
        inst = Institute.objects.get(id=inst_id)
        scientists = (Scientist.objects.filter(institute_id=inst_id)
                      .order_by('name'))
    except:
        return Http404('Институт не найден')
        
    return render(request, 'info/institute_info.html',
                  {
                      'institute': inst,
                      'scientists': scientists
                   })
