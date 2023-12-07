from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .forms import CreateUserForm, CreateGrantForm, CreateInstituteForm
from django.contrib.auth.decorators import login_required, permission_required
from info.models import Grant, Institute


def profile(request):
    return render(request, 'moderators/moder_panel_main.html')


def news(request):
    return render(request, 'moderators/news.html')


def moder_guests(request):
    return render(request, 'moderators/moder_guests.html')


def gzs(request):
    return render(request, 'moderators/gzs.html')


@login_required
@permission_required('auth.create_user', raise_exception=True)
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


@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_new_institute(request):

    if request.method == 'POST':

        form = CreateInstituteForm(request.POST)

        if form.is_valid():

            institute = Institute(name=form.cleaned_data['name'],
                                  description=form.cleaned_data['description'],
                                  emplotees_count=form.cleaned_data['employees_count'],
                                  scientist_count=form.cleaned_data['scientist_count'],
                                  chairman=form.cleaned_data['chairman'],
                                  link=form.cleaned_data['link'],
                                  smu_link=form.cleaned_data['smu_link'])
            institute.save()

            return HttpResponseRedirect('/moderators/account')

    else:
        form = CreateInstituteForm()

    return render(request, 'moderators/create_new_institute.html', {'form': form})
