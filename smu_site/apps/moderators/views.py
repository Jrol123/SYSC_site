from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import (CreateUserForm, CreateGrantForm, CreateInstituteForm, CreateNewsForm, UploadSHCDocForm,
                    CreateScientistForm, UploadDocForm)
from .models import Queue
from documents.models import Doc
from info.models import Grant, Institute, Scientist, ScientistLink
from news.models import News, Image
from SHC.models import Doc as SHCDoc
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import default_storage
from news.models import News, Event, Image


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def profile(request):
    return render(request, 'moderators/moder_panel_main.html')


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def news(request):
    return render(request, 'moderators/news.html')

@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def add_new_documents(request):
    return render(request, 'moderators/add_new_documents.html')

@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def moder_guests(request):
    moder_queue = []
    obtp = {'doc': ('Документ', Doc), 'news': ('Новость', News),
            'event': ('Мероприятие', Event),
            'scientist': ('Учёный', Scientist),
            'grant': ('Грант', Grant)}
    for q in Queue.objects.all():
        moder_queue.append((obtp[q.obj_type][0],
                            obtp[q.obj_type][1]
                            .objects.get(queue_id=q.id)))
    
    return render(request, 'moderators/moder_guests.html',
                  {'queue': moder_queue, 'range': range(20)})


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

    return render(request, 'moderators/gzs.html',
                  {'form': form})


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def add_new_guests(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['user_name'],
                                            password=form.cleaned_data['password'])
            user_group = Group.objects.get(name=form.cleaned_data['user_group'])
            user.groups.add(user_group)
    else:
        form = CreateUserForm()

    return render(request, 'moderators/add_new_guests.html', {'form': form})


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_new_grant(request):

    if request.method == 'POST':

        form = CreateGrantForm(request.POST)

        if form.is_valid():

            grant = Grant(name=form.cleaned_data['name'],
                          criteria=form.cleaned_data['criteria'],
                          description=form.cleaned_data['description'],
                          end_doc_date=form.cleaned_data['end_doc_date'],
                          end_result_date=form.cleaned_data['end_result_date'],
                          link=form.cleaned_data['link'])
            grant.save()

            return HttpResponseRedirect('/moderators/account')  # редирект
    else:
        form = CreateGrantForm()

    return render(request, 'moderators/create_new_grant.html', {'form': form})


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

    return render(request, 'moderators/create_new_institute.html', {'form': form})


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_scientist(request):
    if request.method == 'POST':

        form = CreateScientistForm(request.POST, request.FILES)

        if form.is_valid():
            scientist = Scientist(institute_id=institute_id,
                                  name=form.cleaned_data['name'],
                                  lab=form.cleaned_data['lab'],
                                  position=form.cleaned_data['position'],
                                  degree=form.cleaned_data['degree'],
                                  teaching_info=form.cleaned_data['teaching_info'],
                                  scientific_interests=form.cleaned_data['scientific_interests'],
                                  achievements=form.cleaned_data['achievements'],
                                  future_plans=form.cleaned_data['future_plans'])
            scientist.save()
            link = ScientistLink(scientist_id=scientist.id,
                                 service_name=form.cleaned_data['service_name'],
                                 link=form.cleaned_data['link'])
            link.save()
            img = Image(scientist_id=scientist.id,
                        url_path=request.FILES['url_path'],
                        alt=form.cleaned_data['alt'])
            img.save()

            return HttpResponseRedirect('/moderators/account')

    else:
        form = CreateScientistForm()

    return render(request, 'moderators/create_scientist.html', {'form': form})


# @transaction.atomic
# @login_required
# @permission_required('auth.moderator', raise_exception=True)
# def create_news(request):
#
#     if request.method == 'POST':
#
#         form = CreateNewsForm(request.POST)
#
#         if form.is_valid():
#
#             news = News(title=form.cleaned_data['name'],
#                         text=form.cleaned_data['description'],
#                         pub_date=form.cleaned_data['date'],
#                         link=form.cleaned_data['link'],
#                         user_id=request.user.id)
#             news.save()
#
#             return HttpResponseRedirect('/moderators/account')
#
#     else:
#         form = CreateNewsForm()
#     return render(request, "moderators/news.html", {"form": form})


@transaction.atomic
@login_required
@permission_required('auth.moderator', raise_exception=True)
def upload_doc(request):
    if request.method == "POST":
        form = UploadDocForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Doc(path=request.FILES["path"],
                      name=form.cleaned_data['name'],
                      category=form.cleaned_data['category'])
            doc.save()
            return HttpResponseRedirect('/moderators/account')
    else:
        form = UploadDocForm()
    return render(request, "moderators/upload_doc.html", {"form": form})


@csrf_exempt
@require_POST
def save_news(request):
    try:
        title = request.POST.get('title')
        text = request.POST.get('text')
        image = request.FILES.get('image')  # Получаем файл изображения из request.FILES

        # Создаем объект News
        obj = News(title=title, text=text,
                   user_id=request.user.id)
        obj.save()

        # Если изображение предоставлено, сохраняем его
        if image:
            # Сохраняем файл на сервере
            img = Image(url_path=image,
                        news_id=obj.id)
            img.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    # try:
    #     # Получение содержимого из запроса
    #     data = json.loads(request.body)
    #     title = data.get('title')
    #     text = data.get('text')
    #     image_data = data.get('image')  # получение данных о изображении
    #
    #     # Создаём новость
    #     obj = News(user_id=request.user.id, title=title, text=text)
    #     obj.save()
    #
    #     # Если изображение предоставлено, обрабатываем и сохраняем его
    #     if image_data:
    #         # Декодируем Base64 и создаём ContentFile
    #         format, imgstr = image_data.split(';base64,')  # определение формата изображения и само изображение в формате base64
    #         ext = format.split('/')[-1]  # получаем расширение файла из формата
    #         image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    #
    #         # Сохраняем файл изображения на сервере в заданное место и получаем путь
    #         image_path = default_storage.save('images/news/{}.{}'.format(obj.id, ext), image)
    #
    #         # Создаем объект модели Doc, связанный с новостью и содержащий путь к изображению
    #         doc = Doc(url_path=image_path, news_id=obj.id)
    #         doc.save()
    #
    #     return JsonResponse({'success': True})
    # except Exception as e:
    #     return JsonResponse({'success': False, 'error': str(e)})
