from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from info.models import Institute, Grant
from news.models import Image
from documents.models import Doc
from django.forms import ModelForm


class CreateUserForm(forms.Form):
    user_group = forms.ChoiceField(help_text="Выберите тип аккаунта",
                                   choices=(("representative", "Representative"), ("moderator", "Moderator")))
    user_name = forms.CharField(help_text="Введите имя аккаунта", required=True)
    password = forms.CharField(help_text="Введите пароль", required=True, widget=forms.PasswordInput)
    password_repeat = forms.CharField(help_text="Введите пароль еще раз", required=True, widget=forms.PasswordInput)

    def clean_user_name(self):
        name = self.cleaned_data['user_name']

        name_list = User.objects.values('username')  # список свойств в формате:
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


class CreateGrantForm(ModelForm):
    name = forms.CharField(help_text="Введите название гранта", required=True)
    description = forms.CharField(help_text="Введите описание гранта", widget=forms.Textarea)
    end_doc_date = forms.DateField(help_text="Введите дату окончания приема заявок", required=True,
                                   widget=forms.SelectDateWidget)
    end_result_date = forms.DateField(help_text="Введите дату подведения итогов", required=True,
                                      widget=forms.SelectDateWidget)
    criteria = forms.CharField(help_text="Введите критерии", widget=forms.Textarea)
    link = forms.URLField(help_text="Введите ссылку на грант", required=True)

    class Meta:
        model = Image
        fields = ['name', 'url_path', 'alt', 'description', 'end_doc_date', 'end_result_date', 'criteria', 'link']

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


class CreateInstituteForm(ModelForm):
    name = forms.CharField(help_text="Введите название института", required=True)
    description = forms.CharField(help_text="Введите писание института", widget=forms.Textarea, required=False)
    employees_count = forms.IntegerField(help_text="Введите число сотрудников", required=True)
    scientist_count = forms.IntegerField(help_text="Введите число молодых ученых", required=True)
    chairman = forms.CharField(help_text="Введите ФИО представителя", required=True)
    link = forms.URLField(help_text="Введите ссылку на сайт института", required=True)
    smu_link = forms.URLField(help_text="Введите ссылку на сайт СМУ института", required=False)

    class Meta:
        model = Image
        fields = ['name', 'url_path', 'alt', 'description', 'employees_count',
                  'scientist_count', 'chairman', 'link', 'smu_link']

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


class CreateScientistForm(ModelForm):
    name = forms.CharField(help_text="Введите ФИО учёного", required=True)
    lab = forms.CharField(help_text="?", required=False)
    position = forms.IntegerField(help_text="?", required=True)
    degree = forms.IntegerField(help_text="Введите учёную степень", required=True)
    teaching_info = forms.CharField(help_text="?", required=True, widget=forms.Textarea)
    scientific_interests = forms.CharField(help_text="Интересы", required=True, widget=forms.Textarea)
    achievements = forms.CharField(help_text="Достижения", required=True, widget=forms.Textarea)
    future_plans = forms.CharField(help_text="Планы", required=True, widget=forms.Textarea)
    link = forms.URLField(help_text="Введите ссылку", required=False)
    service_name = forms.CharField(help_text="Введите название сервиса", required=False)

    class Meta:
        model = Image
        fields = ['name', 'url_path', 'alt', 'lab', 'position',
                  'degree', 'teaching_info', 'scientific_interests',
                  'achievements', 'future_plans', 'link', 'service_name']


class CreateNewsForm(forms.Form):
    name = forms.CharField(help_text="Введите название", required=True)
    description = forms.CharField(help_text="Введите текст", widget=forms.Textarea)


class UploadDocForm(ModelForm):
    class Meta:
        model = Doc
        fields = ['name', 'category', 'path']
