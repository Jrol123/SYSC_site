from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import (CreateInstituteForm, CreateNewsForm, CreateGrantForm,
                    CreateScientistForm, UploadDocForm)
from documents.models import Doc
from info.models import Institute, Scientist, ScientistLink, Grant
from news.models import News, Event, Image


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def profile(request):
    return render(request, 'representatives/moder_panel_main.html')


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def news(request):
    return render(request, 'representatives/news.html')


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
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

            return HttpResponseRedirect('/representatives/account')  # редирект
    else:
        form = CreateGrantForm()

    return render(request, 'representatives/create_new_grant.html', {'form': form})


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
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

            return HttpResponseRedirect('/representatives/account')

    else:
        form = CreateInstituteForm()

    return render(request, 'representatives/create_new_institute.html', {'form': form})


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def create_scientist(request):
    if request.method == 'POST':

        form = CreateScientistForm(request.POST, request.FILES)

        if form.is_valid():
            scientist = Scientist(#institute_id=institute_id,
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

            return HttpResponseRedirect('/representatives/account')

    else:
        form = CreateScientistForm()

    return render(request, 'representatives/create_scientist.html', {'form': form})


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def create_news(request):
    if request.method == 'POST':

        form = CreateNewsForm(request.POST)

        if form.is_valid():
            news = News(title=form.cleaned_data['name'],
                        text=form.cleaned_data['description'],
                        pub_date=form.cleaned_data['date'],
                        link=form.cleaned_data['link'],
                        user_id=request.user.id)
            news.save()

            return HttpResponseRedirect('/representatives/account')

    else:
        form = CreateNewsForm()
    return render(request, "representatives/news.html", {"form": form})


@transaction.atomic
@login_required
@permission_required('auth.representative', raise_exception=True)
def upload_doc(request):
    if request.method == "POST":
        form = UploadDocForm(request.POST, request.FILES)
        if form.is_valid():
            doc = Doc(path=request.FILES["path"],
                      name=form.cleaned_data['name'],
                      category=form.cleaned_data['category'])
            doc.save()
            return HttpResponseRedirect('/representatives/account')
    else:
        form = UploadDocForm()
    return render(request, "representatives/upload_doc.html", {"form": form})
