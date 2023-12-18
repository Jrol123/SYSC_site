from django.shortcuts import render, Http404
from info.models import Institute, Scientist, Grant
from news.models import Image


def institutes(request):
    inst = Institute.objects.all().order_by('name')
    inst = [(i, Image.objects.filter(institute_id=i.id)
             .order_by('id').first())
            for i in inst]
    return render(request, 'info/institutes.html',
                  {'institutes': inst,
                   "is_moder": request.user.groups.filter(name='moderator').exists(),
                   "is_repr": request.user.groups.filter(name='representative').exists()
                   })


def grant(request):
    grants = (Grant.objects.filter(queue_id__isnull=True)
              .order_by('end_doc_date'))
    grants = [(g, Image.objects.filter(grant_id=g.id)
               .order_by('id').first())
              for g in grants]
    return render(request, 'info/grant.html',
                  {'grants': grants,
                   "is_moder": request.user.groups.filter(name='moderator').exists(),
                   "is_repr": request.user.groups.filter(name='representative').exists()
                   })


def organization(request):
    return render(request, 'info/organization.html',{
                      "is_moder": request.user.groups.filter(name='moderator').exists(),
                      "is_repr": request.user.groups.filter(name='representative').exists()})


def institute_info(request, inst_id):
    try:
        inst = Institute.objects.get(id=inst_id)
    except:
        return Http404('Институт не найден')

    inst_img = Image.objects.filter(institute_id=inst_id).first()
    scientists = (Scientist.objects.filter(institute_id=inst_id)
                  .order_by('name'))
    scientists = [(s, Image.objects.filter(scientist_id=s.id)
                   .order_by('id').first())
                  for s in scientists]
    return render(request, 'info/institute_info.html',
                  {
                      'institute': inst,
                      'inst_img': inst_img,
                      'scientists': scientists,
                      "is_moder": request.user.groups.filter(name='moderator').exists(),
                      "is_repr": request.user.groups.filter(name='representative').exists()
                  })
