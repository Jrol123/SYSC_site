from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from info.models import Institute

class CreateUserForm(forms.Form):
    user_group = forms.ChoiceField(help_text="Выберите тип аккаунта", required=False,
                                   choices=(("representative", "Representative"), ("moderator", "Moderator")))
    user_name = forms.CharField(help_text="Введите имя аккаунта", required=True)
    password = forms.CharField(help_text="Введите пароль", required=True, widget=forms.PasswordInput)
    password_repeat = forms.CharField(help_text="Введите пароль еще раз", required=True, widget=forms.PasswordInput)

    def clean_user_name(self):
        name = self.cleaned_data['user_name']

        name_list = User.objects.values('username') # список свойств в формате:
        # [{'username': 'MyUsername1'}, {'username': 'MyUsername2'}, ...]
        for val in name_list:
            if name == val['username']:
                raise ValidationError('Такой username уже существует')

        return name

    def clean_password(self):
        password = self.cleaned_data['password']

        return password

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        password_rep = self.cleaned_data['password_repeat']

        if password_rep != password:
            raise ValidationError('Пароли должны совпадать')

        return password_rep

    def clean_user_group(self):
        group = self.cleaned_data['user_group']

        return group


class CreateInstituteForm(forms.Form):
    name = forms.CharField(help_text="Введите название института", required=True)
    description = forms.CharField(help_text="Введите писание института", widget=forms.Textarea, required=False)
    employees_count = forms.IntegerField(help_text="Введите число сотрудников", required=True)
    scientist_count = forms.IntegerField(help_text="Введите число молодых ученых", required=True)
    chairman = forms.CharField(help_text="Введите ФИО представителя", required=True)
    link = forms.URLField(help_text="Введите ссылку на сайт института", required=True)
    smu_link = forms.URLField(help_text="Введите ссылку на сайт СМУ института", required=False)

    def clean_name(self):
        name = self.cleaned_data['name']

        name_list = Institute.objects.values('name')  # список свойств в формате:
        # [{'name': 'Name1'}, {'name': 'Name2'}, ...]
        for val in name_list:
            if name == val['name']:
                raise ValidationError('Такое название уже существует')

        return name

    def clean_employees_count(self):
        employees_count = self.cleaned_data['employees_count']
        if employees_count < 1:
            raise ValidationError('Количество сотрудников не может быть меньше 1')
        return employees_count

    def clean_scientist_count(self):
        scientist_count = self.cleaned_data['scientist_count']
        if scientist_count < 0:
            raise ValidationError('Количество сотрудников не может быть отрицательным')
        return scientist_count

    def clean_chairman(self):
        chairman = self.cleaned_data['chairman']
        return chairman

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_link(self):
        link = self.cleaned_data['link']
        return link

    def clean_smu_link(self):
        link = self.cleaned_data['smu_link']
        return link
