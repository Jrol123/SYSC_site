from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'moderator'


def profile(request):
    return render(request, 'moderators/main_moder_panel.html')


@login_required
@permission_required('auth.create_user', raise_exception=True)
def create_new_user(request):

    # Если данный запрос типа POST
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса
        form = CreateUserForm(request.POST)

        # Проверка валидности данных формы
        if form.is_valid():

            # Создаиение пользователя и сохранение его в базе данных
            user = User.objects.create_user(username=form.cleaned_data['user_name'],
                                     password=form.cleaned_data['password'])
            user_group = Group.objects.get(name=form.cleaned_data['user_group'])
            user.groups.add(user_group)
            return HttpResponseRedirect('/moderators/account')  # редирект



    # Если это GET - создать форму по умолчанию
    else:
        form = CreateUserForm()

    return render(request, 'moderators/create_new_user.html', {'form': form})
