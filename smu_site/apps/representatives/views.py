from django.contrib.auth.decorators import login_required, \
    permission_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .forms import CreateScientistForm, UploadDocForm
from documents.models import Doc, Category
from info.models import Institute, Scientist, ScientistLink
from moderators.models import Queue
from news.models import News, Event, Image
from representatives.models import ReprInst


# @transaction.atomic
# @login_required
# @permission_required('auth.representative', raise_exception=True)
# def news(request):
#     return render(request, 'representatives/news.html', {
#         "is_moder": request.user.groups.filter(name='moderator').exists(),
#         "is_repr": request.user.groups.filter(name='representative').exists()
#     })


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def create_scientist(request):
    if request.method == 'POST':
        form = CreateScientistForm(request.POST, request.FILES)
        if form.is_valid():
            q = Queue(obj_type='scientist')
            q.save()
            
            scientist = Scientist(
                institute_id=ReprInst.objects.get(
                    user_id=request.user.id).institute_id,
                queue_id=q.id,
                user_id=request.user.id,
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
            
            return HttpResponseRedirect(
                '/representatives/account',
                {"is_moder": request.user.groups
                      .filter(name='moderator').exists(),
                      "is_repr": request.user.groups
                      .filter(name='representative').exists(),})
    
    else:
        form = CreateScientistForm()
    
    return render(request, 'representatives/create_scientist.html', {
        'form': form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })


# @transaction.atomic
# @login_required
# @permission_required('auth.representative', raise_exception=True)
# def create_news(request):
#     if request.method == 'POST':
#         form = CreateNewsForm(request.POST)
#
#         if form.is_valid():
#             q = Queue(obj_type='news')
#             q.save()
#
#             news = News(title=form.cleaned_data['name'],
#                         text=form.cleaned_data['description'],
#                         pub_date=form.cleaned_data['date'],
#                         link=form.cleaned_data['link'],
#                         user_id=request.user.id, queue_id=q.id)
#             news.save()
#
#             return HttpResponseRedirect('/representatives/account')
#
#     else:
#         form = CreateNewsForm()
#
#     return render(request, "representatives/news.html",
#                   {"form": form})


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def create_news(request):
    return render(request, "representatives/news.html", {
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
            q = Queue(obj_type='event')
            q.save()
            
            start = request.POST.get('start')
            end = request.POST.get('end')
            obj = Event(queue_id=q.id, title=title, text=text,
                        user_id=request.user.id,
                        begin_date=start, end_date=end)
            obj.save()
            
            try:
                img = Image(url_path=image, event_id=obj.id)
                img.save()
            except:
                pass
        else:
            q = Queue(obj_type='news')
            q.save()
            
            obj = News(queue_id=q.id, title=title, text=text,
                       user_id=request.user.id)
            obj.save()
            
            try:
                img = Image(url_path=image, news_id=obj.id)
                img.save()
            except:
                pass

        return JsonResponse({'success': True})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def upload_doc(request):
    if request.method == "POST":
        form = UploadDocForm(request.POST, request.FILES)
        if form.is_valid():
            q = Queue(obj_type='doc')
            q.save()
            
            if form.cleaned_data['Choose_Category'] == 'True':
                cat = Category(name=form.cleaned_data['New_category'])
                cat.save()
                doc = Doc(path=request.FILES["path"],
                          name=form.cleaned_data['name'],
                          category_id=cat.id, user_id=request.user.id,
                          queue_id=q.id)
                doc.save()
            else:
                doc = Doc(path=request.FILES["path"],
                          name=form.cleaned_data['name'],
                          category_id=form.cleaned_data['Category'],
                          user_id=request.user.id, queue_id=q.id)
                doc.save()
            
            return HttpResponseRedirect('/representatives/account')
        
        # if form.is_valid():
        #     q = Queue(obj_type='doc')
        #     q.save()
        #
        #     doc = Doc(path=request.FILES["path"],
        #               name=form.cleaned_data['name'],
        #               category=form.cleaned_data['category'],
        #               queue_id=q.id)
        #     doc.save()
        #     return HttpResponseRedirect('/representatives/account')
    else:
        form = UploadDocForm()
    
    return render(request, "representatives/upload_doc.html", {
        "form": form,
        "is_moder": request.user.groups.filter(name='moderator').exists(),
        "is_repr": request.user.groups.filter(name='representative').exists()
    })
