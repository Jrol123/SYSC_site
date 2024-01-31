from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import connection
from django.forms import ModelForm
from documents.models import Doc, Category
from info.models import Institute, Grant
from news.models import Image
from SHC.models import Doc as SHCDoc


class CreateUserForm(forms.Form):
    def get_dynamic_choices(self):
        INSTITUTE_CHOICE = []
        if Institute._meta.db_table in connection.introspection.table_names():
            institutes_list = Institute.objects.values('id', 'name')
            for obj in institutes_list:
                INSTITUTE_CHOICE.append((obj['id'], obj['name']))
        return INSTITUTE_CHOICE

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['user_group'] = forms.ChoiceField(
            help_text="Выберите тип аккаунта",
            choices=(
                ("representative", "Представитель"),
                ("moderator", "Модератор")),
            widget=forms.Select(attrs={
                'class': "form-control input_for_form",
                'id': "userGroup", 'name': "userGroup"
            }))
        self.fields['user_institute'] = forms.ChoiceField(
            help_text="Выберите институт",
            choices=self.get_dynamic_choices(),
            widget=forms.Select(attrs={
                'class': "form-control input_for_form",
                'id': "institute", 'name': "institute"
            }))
        self.fields['user_name'] = forms.CharField(
            help_text="Введите имя аккаунта",
            required=True,
            widget=forms.TextInput(attrs={
                'type': "text",
                'class': "form-control input_for_form",
                'id': "username", 'name': "username",
            }))
        self.fields['email'] = forms.EmailField(
            help_text="Введите имя аккаунта",
            required=True,
            widget=forms.EmailInput(attrs={
                'type': "email",
                'class': "form-control input_for_form",
                'id': "Email", 'name': "Email",
            }))
        self.fields['password'] = forms.CharField(
            help_text="Введите пароль",
            required=True,
            widget=forms.PasswordInput(attrs={
                'type': "password",
                'class': "form-control input_for_form",
                'id': "password", 'name': "password"
            }))
        self.fields['password_repeat'] = forms.CharField(
            help_text="Введите пароль еще раз", required=True,
            widget=forms.PasswordInput(attrs={
                'type': "password",
                'class': "form-control input_for_form",
                'id': "confirmPassword", 'name': "confirmPassword"
            }))

    def clean_user_name(self):
        name = self.cleaned_data['user_name']

        name_list = User.objects.values('username')  # список свойств в формате:
        # [{'username': 'MyUsername1'}, {'username': 'MyUsername2'}, ...]
        for val in name_list:
            if name == val['username']:
                raise ValidationError('Такой username уже существует')

        return name

    def clean_password(self):
        return self.cleaned_data['password']

    def clean_password_repeat(self):
        password = self.cleaned_data['password']
        password_rep = self.cleaned_data['password_repeat']

        if password_rep != password:
            raise ValidationError('Пароли должны совпадать')

        return password_rep

    def clean_user_group(self):
        group = self.cleaned_data['user_group']

        return group

    def clean_email(self):
        email = self.cleaned_data['email']

        return email


class CreateGrantForm(ModelForm):
    name = forms.CharField(
        help_text="Введите название гранта",
        required=True, widget=forms.TextInput(attrs={
            'class': "input_for_form",
            'id': "grant_name", 'name': "grant_name",
            'type': "text"
        }))
    description = forms.CharField(
        help_text="Введите описание гранта",
        widget=forms.Textarea(attrs={
            'class': "textarea m-1 col-lg-12 col-sm-12 col-md-12 col-xs-12",
            'id': "description", 'name': "description",
        }))
    end_doc_date = forms.DateTimeField(
        help_text="Введите дату окончания приема заявок", required=True,
        widget=forms.TextInput(attrs={
            'class': "input_for_form",
            'id': "start_date", 'name': "start_date",
            'type': "datetime-local", 'step': "60"
        }))
    end_result_date = forms.DateTimeField(
        help_text="Введите дату подведения итогов", required=True,
        widget=forms.TextInput(attrs={
            'class': "input_for_form",
            'id': "end_date", 'name': "end_date",
            'type': "datetime-local", 'step': "60"
        }))
    criteria = forms.CharField(
        help_text="Введите критерии",
        widget=forms.Textarea(attrs={
            'class': "textarea m-1 col-lg-12 col-sm-12 col-md-12 col-xs-12",
            'id': "criteria", 'name': "criteria",
        }))
    link = forms.URLField(
        help_text="Введите ссылку на грант",
        required=True, widget=forms.URLInput(attrs={
            'class': "input_for_form",
            'id': "grant_link", 'name': "grant_link",
            'type': "url"
        }))

    class Meta:
        model = Image
        fields = ['name', 'url_path', 'description',
                  'end_doc_date', 'end_result_date', 'criteria', 'link']
        widgets = {'url_path': forms.FileInput(attrs={
            'class': "input_for_form_img", 'type': "file",
            'id': "imageInput", 'name': "image",
            'accept': ".jpg, .jpeg, .png"
        })}

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


class CreateInstituteForm(forms.Form):
    name = forms.CharField(help_text="Введите название института",
                           widget=forms.TextInput(
                               attrs={'class': "input_for_form",
                                      'type': "text", 'id': "inst_name",
                                      'name': "grant_name"}),
                           required=True)
    description = forms.CharField(
        help_text="Введите писание института",
        widget=forms.Textarea(attrs={
            'class': "textarea m-1 col-lg-12 col-sm-12 col-md-12 "
                     "col-xs-12",
            'id': "description", 'name': "description"}),
        required=True)
    employees_count = forms.IntegerField(
        help_text="Введите число сотрудников",
        widget=forms.NumberInput(attrs={
            'type': "number", 'class': "input_for_form",
            'id': "numberInput", 'placeholder': "Введите число",
            'min': "0"}), required=True)
    scientist_count = forms.IntegerField(
        help_text="Введите число молодых ученых",
        widget=forms.NumberInput(attrs={
            'type': "number", 'class': "input_for_form",
            'id': "numberInput2", 'placeholder': "Введите число",
            'min': "0"}), required=True)
    chairman = forms.CharField(help_text="Введите ФИО представителя",
                               widget=forms.TextInput(
                                   attrs={'type': "text",
                                          'class': "input_for_form",
                                          'id': "chairman",
                                          'name': "Chairman"}),
                               required=True)
    link = forms.URLField(help_text="Введите ссылку на сайт института",
                          widget=forms.URLInput(
                              attrs={'class': "input_for_form",
                                     'type': "url",
                                     'id': "institute_link",
                                     'name': "institute_link"}),
                          required=True)
    smu_link = forms.URLField(
        help_text="Введите ссылку на сайт СМУ института",
        widget=forms.URLInput(attrs={
            'class': "input_for_form", 'type': "url",
            'id': "smu_link", 'name': "smu_link"}), required=False)

    img = forms.ImageField(help_text="Изображение Института",
                           widget=forms.FileInput(
                               attrs={'class': "input_for_form_img",
                                      'type': "file",
                                      'id': "imageInput",
                                      'name': "image",
                                      'onchange' : "checkImageSize(this)",
                                      'accept': ".jpg, .jpeg, .png"}),
                           required=True)

    # class Meta:
    #     model = Image
    #     fields = ['name', 'url_path', 'alt', 'description',
    #               'employees_count',
    #               'scientist_count', 'chairman', 'link', 'smu_link']

    def clean_name(self):
        name = self.cleaned_data['name']

        name_list = Institute.objects.values(
            'name')  # список свойств в формате:
        # [{'name': 'Name1'}, {'name': 'Name2'}, ...]
        for val in name_list:
            if name == val['name']:
                raise ValidationError('Такое название уже существует')

        return name

    def clean_employees_count(self):
        employees_count = self.cleaned_data['employees_count']
        if employees_count < 1:
            raise ValidationError(
                'Количество сотрудников не может быть меньше 1')
        return employees_count

    def clean_scientist_count(self):
        scientist_count = self.cleaned_data['scientist_count']
        if scientist_count < 0:
            raise ValidationError(
                'Количество сотрудников не может быть отрицательным')
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

    def save(self, commit=True):
        cd = self.cleaned_data
        url_path = cd['img']

        inst = Institute(name=cd['name'], description=cd['description'],
                         employees_count=cd['employees_count'],
                         scientist_count=cd['scientist_count'],
                         chairman=cd['chairman'],
                         link=cd['link'], smu_link=cd['smu_link'])
        if commit:
            inst.save()

            img = Image(institute_id=inst.id, alt=cd['name'])
            img.url_path.save(url_path.name, url_path, save=True)

        return inst


class CreateScientistForm(ModelForm):
    def get_dynamic_choices(self):
        INSTITUTE_CHOICE = []
        if Institute._meta.db_table in connection.introspection.table_names():
            institutes_list = Institute.objects.values('id', 'name')
            for obj in institutes_list:
                INSTITUTE_CHOICE.append((obj['id'], obj['name']))
                
        return INSTITUTE_CHOICE

    def __init__(self, *args, **kwargs):
        super(CreateScientistForm, self).__init__(*args, **kwargs)

        self.fields['name'] = forms.CharField(
            widget=forms.TextInput(attrs=
                                   {'class': "input_for_form",
                                    'type': "text",
                                    'placeholder': "Введите ФИО учёного"}),
            required=True)

        self.fields['lab'] = forms.CharField(widget=forms.TextInput(
            attrs={'class': "input_for_form",
                   'type': "text",
                   }),
            required=True)

        self.fields['position'] = forms.CharField(widget=forms.TextInput(
            attrs={'class': "input_for_form",
                   'type': "text",
                   'placeholder': "Введите должность"}),
            required=True)

        self.fields['degree'] = forms.CharField(widget=forms.TextInput(
            attrs={'class': "input_for_form",
                   'type': "text",
                   }),
            required=True)

        self.fields['scientific_interests'] = forms.CharField(
            widget=forms.Textarea(
                attrs={'class': "input_for_form",
                       'type': "text",
                       }),
            required=True)

        self.fields['link'] = forms.CharField(widget=forms.Textarea(
            attrs={'class': "input_for_form",
                   'type': "text",
                   }),
            required=True)

        # self.fields['service_name'] = forms.CharField(widget=forms.Textarea(
        #     attrs={'class': "input_for_form",
        #            'type': "text",
        #            }),
        #     required=True)

        self.fields['institute'] = forms.ChoiceField(widget=forms.Select(
            attrs={'class': "input_for_form col-lg-11 col-sm-11 col-md-11 col-xs-11",
                   }),
            required=True,
            choices=self.get_dynamic_choices())

    class Meta:
        model = Image
        fields = ['url_path']
        widgets = {'url_path': forms.FileInput(
            attrs={'class': "input_for_form_img",
                   'type': "file",
                   'id': "imageInput",
                   'name': "image",
                   'accept': ".jpg, .jpeg, .png"})}

    def clean_name(self):
        return self.cleaned_data['name']

    def clean_lab(self):
        return self.cleaned_data['lab']

    def clean_position(self):
        return self.cleaned_data['position']

    def clean_degree(self):
        return self.cleaned_data['degree']

    def clean_link(self):
        return self.cleaned_data['link']

    def clean_scientific_interests(self):
        return self.cleaned_data['scientific_interests']

    def clean_institute(self):
        return self.cleaned_data['institute']


# class CreateNewsForm(forms.Form):
#     name = forms.CharField(help_text="Введите название", required=True)
#     description = forms.CharField(help_text="Введите текст",
#                                   widget=forms.Textarea)


class UploadDocForm(ModelForm):
    def get_dynamic_choices(self):
        CATEGORY_CHOICE = []
        if Category._meta.db_table in connection.introspection.table_names():
            categories_list = Category.objects.values('id', 'name')
            for obj in categories_list:
                CATEGORY_CHOICE.append((obj['id'], obj['name']))
        return CATEGORY_CHOICE

    def __init__(self, *args, **kwargs):
        super(UploadDocForm, self).__init__(*args, **kwargs)

        self.fields['Choose_Category'] = forms.ChoiceField(widget=forms.Select(
            attrs={'class': "form-control input_for_form text-dark",
                   }),
            required=True,
            choices=((True, 'Да'), (False, 'Нет')))
        self.fields['Category'] = forms.ChoiceField(widget=forms.Select(
            attrs={'class': "form-control input_for_form text-dark",
                   }),
            required=False,
            choices=self.get_dynamic_choices())
        self.fields['New_category'] = forms.CharField(widget=forms.TextInput(
            attrs={'class': "form-control input_for_form",
                   'type': "text"
                   }),
            required=False)

    class Meta:
        model = Doc
        fields = ['name', 'path']  # 'category'
        widgets = {
            'path': forms.FileInput(
                attrs={'class': "mt-2 input_for_form_img col-lg-6 col-sm-6 col-md-6 col-xs-6",
                       'type': "file",
                       'id': "documentUpload",
                       'name': "documentUpload",
                       'accept': ".doc, .docx, .xls, .txt, .rtf, .pdf"}),
            'name': forms.TextInput(
                attrs={'class': "form-control input_for_form",
                       'type': "text"})
        }


class UploadSHCDocForm(forms.Form):
    name = forms.CharField(
        help_text='Название документа',
        widget=forms.TextInput(attrs={
            'class': "input_for_form col-lg-3 col-sm-3 col-md-3 "
                     "col-xs-3",
            'type': "text", 'id': "grant_name", 'name': "doc_name"}),
        required=True)
    path = forms.FileField(
        help_text='Загрузить документ',
        widget=forms.FileInput(attrs={
            'class': "input_for_form_img col-lg-6 col-sm-6 col-md-6 "
                     "col-xs-6",
            'type': "file",
            'accept': ".doc, .docx, .xls, .txt, .rtf, .pdf",
            'id': "documentUpload", 'name': "documentUpload"}),
        required=True)
    description = forms.CharField(
        help_text='Описание',
        widget=forms.Textarea(attrs={
            'class': "textarea col-lg-12 col-sm-12 col-md-12 col-xs-12",
            'id': "description", 'name': "description"}), required=True)

    def save(self, commit=True):
        name = self.cleaned_data['name']
        path = self.cleaned_data['path']
        description = self.cleaned_data['description']

        if not Category.objects.filter(name='ГЖС').exists():
            c = Category(name='ГЖС')
            c.save()

        doc = Doc(name=name,
                  category_id=Category.objects.get(name='ГЖС').id)
        if commit:
            # Создаем объект Doc из documents.models и сохраняем файл
            doc.path.save(path.name, path, save=True)

            shc_doc = SHCDoc(doc=doc, description=description)
            shc_doc.save()

        return doc
