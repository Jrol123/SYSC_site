from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .forms import CreateUserForm, CreateInstituteForm
from django.contrib.auth.decorators import login_required, permission_required
from info.models import Institute

app_name = 'moderator'


@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_new_user(request):

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(username=form.cleaned_data['user_name'],
                                     password=form.cleaned_data['password'])
            user_group = Group.objects.get(name=form.cleaned_data['user_group'])
            user.groups.add(user_group)
            return HttpResponseRedirect('/moderators/account')

    else:
        form = CreateUserForm()

    return render(request, 'moderators/create_new_user.html', {'form': form})


@login_required
@permission_required('auth.moderator', raise_exception=True)
def create_new_institute(request):

    if request.method == 'POST':

        form = CreateInstituteForm(request.POST)

        if form.is_valid():

            institute = Institute(name=form.cleaned_data['name'],
                                  description=form.cleaned_data['description'],
                                  structure=form.cleaned_data['structure'],
                                  link=form.cleaned_data['link'])
            institute.save()

            return HttpResponseRedirect('/moderators/account')

    else:
        form = CreateInstituteForm()

    return render(request, 'moderators/create_new_user.html', {'form': form})
