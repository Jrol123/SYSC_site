from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class CreateUserForm(forms.Form):
    user_group = forms.ChoiceField(help_text="Выберите тип аккаунта",
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


class CreateGrantForm(forms.Form):
    name = forms.CharField(help_text="Введите название гранта", required=True)
    description = forms.CharField(help_text="Введите описание гранта", widget=forms.Textarea)
    end_doc_date = forms.DateField(help_text="Введите дату окончания приема заявок", required=True,
                                   widget=forms.SelectDateWidget)
    end_result_date = forms.DateField(help_text="Введите дату подведения итогов", required=True,
                                      widget=forms.SelectDateWidget)
    criteria = forms.CharField(help_text="Введите критерии", widget=forms.Textarea)
    link = forms.URLField(help_text="Введите ссылку на грант", required=True)

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_structure(self):
        criteria = self.cleaned_data['criteria']
        return criteria

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def clean_link(self):
        link = self.cleaned_data['link']
        return link

    def clean_end_doc_date(self):
        end_doc_date = self.cleaned_data['end_doc_date']
        return end_doc_date

    def clean_end_result_date(self):
        end_result_date = self.cleaned_data['end_result_date']
        return end_result_date
