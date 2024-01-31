import configparser

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, Http404

from info.models import Institute, Scientist, Grant
from news.models import Image
from SHC.models import Doc as SHCDoc


config = configparser.ConfigParser()
config.read('config.ini')


# def newspage(request):
#     return render(request, 'info/newspage.html')

def institutes(request):
    inst = Institute.objects.all().order_by('name')
    inst = [(i, Image.objects.filter(institute_id=i.id)
             .order_by('id').first())
            for i in inst]
    return render(request, 'info/institutes.html',
                  {'institutes': inst,
                   "is_moder": request.user.groups.filter(
                       name='moderator').exists(),
                   "is_repr": request.user.groups.filter(
                       name='representative').exists()
                   })


def grant(request):
    grants = (Grant.objects.filter(queue_id__isnull=True)
              .order_by('end_doc_date'))
    grants = [(g, Image.objects.filter(grant_id=g.id)
               .order_by('id').first())
              for g in grants]
    
    p = Paginator(grants, int(config["news"]["grants_per_page"]))
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        # Если page_number не является целым числом, то присваивается 1
        page_obj = p.page(1)
    except EmptyPage:
        # Если страница пустая, возвращает последнюю страницу
        page_obj = p.page(p.num_pages)
        
    return render(request, 'info/grant.html',
                  {'grants': page_obj,
                   "is_moder": request.user.groups
                   .filter(name='moderator').exists(),
                   "is_repr": request.user.groups
                   .filter(name='representative').exists()
                   })


def organization(request):
    return render(request, 'info/organization.html',
                  {
                      "is_moder": request.user.groups
                      .filter(name='moderator').exists(),
                      "is_repr": request.user.groups
                      .filter(name='representative').exists()})


def gzs(request):
    documents = (SHCDoc.objects.select_related('doc')
                 .filter(doc__queue_id__isnull=True)
                 .order_by('doc__id'))
    return render(request, 'info/gzs.html',
                  {
                      'docs': documents,
                      'media': settings.MEDIA_URL,
                      "is_moder": request.user.groups
                      .filter(name='moderator').exists(),
                      "is_repr": request.user.groups
                      .filter(name='representative').exists()})


def institute_info(request, inst_id):
    try:
        inst = Institute.objects.get(id=inst_id)
    except:
        return Http404('Институт не найден')
    
    inst_img = Image.objects.filter(institute_id=inst_id).first()
    scientists = (Scientist.objects.filter(institute_id=inst_id,
                                           queue_id__isnull=True)
                  .order_by('name'))
    scientists = [(s, Image.objects.filter(scientist_id=s.id)
                   .order_by('id').first())
                  for s in scientists]
    return render(request, 'info/institute_info.html',
                  {
                      'institute': inst,
                      'inst_img': inst_img,
                      'scientists': scientists,
                      "is_moder": request.user.groups.filter(
                          name='moderator').exists(),
                      "is_repr": request.user.groups.filter(
                          name='representative').exists()
                  })
