from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from .forms import (CreateUserForm, CreateGrantForm, CreateInstituteForm, UploadSHCDocForm,
                    CreateScientistForm, UploadDocForm)
from .models import Queue
from documents.models import Doc, Category
from info.models import Grant, Institute, Scientist, ScientistLink
from news.models import News, Event, Image
from representatives.models import ReprInst
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# import json
# from django.views import View
# from django.core.files.base import ContentFile
# import base64
# from django.core.files.storage import default_storage


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def add_new_documents(request):
    if request.method == "POST":
        form = UploadDocForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['Choose_Category'] == 'True':
                cat = Category(name=form.cleaned_data['New_category'])
                cat.save()
                doc = Doc(path=request.FILES["path"],
                          name=form.cleaned_data['name'],
                          category_id=cat.id, user_id=request.user.id)
                doc.save()
            else:
                doc = Doc(path=request.FILES["path"],
                          name=form.cleaned_data['name'],
                          category_id=form.cleaned_data['Category'],
                          user_id=request.user.id)
                doc.save()
                
            return HttpResponseRedirect('/moderators/account')
    else:
        form = UploadDocForm()
        
    return render(request, "moderators/add_new_documents.html", {
        "form": form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def moder_guests(request):
    moder_queue = []
    obtp = {'doc': ('Документ', Doc),
            'news': ('Новость', News),
            'event': ('Мероприятие', Event),
            'scientist': ('Учёный', Scientist)}
    for q in Queue.objects.all():
        try:
            moder_queue.append((obtp[q.obj_type][0],
                                obtp[q.obj_type][1]
                                .objects.get(queue_id=q.id)))
        except:
            q.delete()

    return render(request, 'moderators/moder_guests.html', {
        'queue': moder_queue, 'range': range(20),
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def gzs(request):
    if request.method == 'POST':
        form = UploadSHCDocForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/moderators/account')
    else:
        form = UploadSHCDocForm()

    return render(request, 'moderators/gzs.html', {
        'form': form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def add_new_guests(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['user_name'],
                                            email=form.cleaned_data['email'],
                                            password=form.cleaned_data['password'])
            user_group = Group.objects.get(name=form.cleaned_data['user_group'])
            user.groups.add(user_group)
            rep_inst = ReprInst(
                user_id=user.id,
                institute_id=form.cleaned_data['user_institute'])
            rep_inst.save()
    else:
        form = CreateUserForm()

    return render(request, 'moderators/add_new_guests.html', {
        'form': form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_new_grant(request):
    if request.method == 'POST':

        form = CreateGrantForm(request.POST, request.FILES)

        if form.is_valid():
            grant = Grant(name=form.cleaned_data['name'],
                          criteria=form.cleaned_data['criteria'],
                          description=form.cleaned_data['description'],
                          end_doc_date=form.cleaned_data['end_doc_date'],
                          end_result_date=form.cleaned_data['end_result_date'],
                          link=form.cleaned_data['link'])
            grant.save()
            img = Image(grant_id=grant.id,
                        url_path=request.FILES['url_path'])
            img.save()

            return HttpResponseRedirect('/moderators/account')  # редирект
    else:
        form = CreateGrantForm()

    return render(request, 'moderators/create_new_grant.html', {
        'form': form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_new_institute(request):
    if request.method == 'POST':
        form = CreateInstituteForm(request.POST, request.FILES)
        if form.is_valid():
            # institute = Institute(name=form.cleaned_data['name'],
            #                       description=form.cleaned_data['description'],
            #                       emplotees_count=form.cleaned_data['employees_count'],
            #                       scientist_count=form.cleaned_data['scientist_count'],
            #                       chairman=form.cleaned_data['chairman'],
            #                       link=form.cleaned_data['link'],
            #                       smu_link=form.cleaned_data['smu_link'])
            # institute.save()
            form.save()

            return HttpResponseRedirect('/moderators/account')

    else:
        form = CreateInstituteForm()

    return render(request, 'moderators/create_new_institute.html', {
        'form': form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_scientist(request):
    if request.method == 'POST':

        form = CreateScientistForm(request.POST, request.FILES)

        if form.is_valid():
            print(repr(form.cleaned_data['institute']))
            scientist = Scientist(institute_id=form.cleaned_data['institute'],
                                  name=form.cleaned_data['name'],
                                  lab=form.cleaned_data['lab'],
                                  position=form.cleaned_data['position'],
                                  degree=form.cleaned_data['degree'],
                                  scientific_interests=form.cleaned_data['scientific_interests'],
                                  user_id=request.user.id)
            scientist.save()
            
            links = form.cleaned_data['link'].split('\n')
            for link in links:
                desc, link = link.rsplit(' ', 1)
                lnk = ScientistLink(scientist_id=scientist.id,
                                    link=link, service_name=desc)
                lnk.save()
                
            img = Image(scientist_id=scientist.id,
                        url_path=request.FILES['url_path'],
                        alt=form.cleaned_data['name'])
            img.save()
        # else:
        #     res = 'o_o\n'
        #     for e in form.errors:
        #         res += str(e)
        #     return HttpResponse(res)

    else:
        form = CreateScientistForm()

    return render(request, 'moderators/create_scientist.html', {
            'form': form,
            "is_moder": request.user.groups.filter(name='moderator').exists(),
            "is_repr": request.user.groups.filter(name='representative').exists()
        })


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_news(request):
    return render(request, "moderators/news.html",
                  {
                      "is_moder": request.user.groups.filter(name='moderator').exists(),
                      "is_repr": request.user.groups.filter(name='representative').exists()
                  })


@csrf_exempt
@transaction.atomic
@require_POST
def save_news(request):
    try:
        # Получение содержимого из запроса
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        if category == 'Events':
            start = request.POST.get('start')
            end = request.POST.get('end')
            obj = Event(title=title, text=text,
                        user_id=request.user.id,
                        begin_date=start,
                        end_date=end)
            obj.save()
            img = Image(url_path=image, event_id=obj.id)
            img.save()
        else:
            obj = News(title=title, text=text,
                       user_id=request.user.id)
            obj.save()
            img = Image(url_path=image, news_id=obj.id)
            img.save()

        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

# @transaction.atomic
# @login_required
# @permission_required('auth.moderator', raise_exception=True)
# def upload_doc(request):
#     if request.method == "POST":
#         form = UploadDocForm(request.POST, request.FILES)
#         if form.is_valid():
#             doc = Doc(path=request.FILES["path"],
#                       name=form.cleaned_data['name'],
#                       category=form.cleaned_data['category'])
#             doc.save()
#             return HttpResponseRedirect('/moderators/account')
#     else:
#         form = UploadDocForm()
#     return render(request, "moderators/add_new_documents.html",
#                   {"form": form})
