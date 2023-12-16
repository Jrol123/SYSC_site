from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from documents.models import Doc
from info.models import Institute, Grant
from news.models import Image
from SHC.models import Doc as SHCDoc


class CreateUserForm(forms.Form):
    user_group = forms.ChoiceField(help_text="Выберите тип аккаунта",
                                   choices=(
                                       ("representative", "Representative"),
                                       ("moderator", "Moderator")))
    user_name = forms.CharField(help_text="Введите имя аккаунта",
                                required=True)
    password = forms.CharField(help_text="Введите пароль",
                               required=True,
                               widget=forms.PasswordInput)
    password_repeat = forms.CharField(
        help_text="Введите пароль еще раз", required=True,
        widget=forms.PasswordInput)
    
    def clean_user_name(self):
        name = self.cleaned_data['user_name']
        
        name_list = User.objects.values(
            'username')  # список свойств в формате:
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
    name = forms.CharField(help_text="Введите название гранта",
                           required=True)
    description = forms.CharField(help_text="Введите описание гранта",
                                  widget=forms.Textarea)
    end_doc_date = forms.DateField(
        help_text="Введите дату окончания приема заявок", required=True,
        widget=forms.SelectDateWidget)
    end_result_date = forms.DateField(
        help_text="Введите дату подведения итогов", required=True,
        widget=forms.SelectDateWidget)
    criteria = forms.CharField(help_text="Введите критерии",
                               widget=forms.Textarea)
    link = forms.URLField(help_text="Введите ссылку на грант",
                          required=True)
    
    class Meta:
        model = Image
        fields = ['name', 'url_path', 'alt', 'description',
                  'end_doc_date', 'end_result_date', 'criteria', 'link']
        
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
    name = forms.CharField(widget=forms.TextInput(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      'placeholder': "Введите ФИО учёного"}),
                           required=True)

    lab = forms.CharField(widget=forms.TextInput(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    position = forms.CharField(widget=forms.TextInput(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      'placeholder': "Введите должность"}),
                           required=True)

    degree = forms.IntegerField(widget=forms.NumberInput(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    teaching_info = forms.CharField(widget=forms.Textarea(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    scientific_interests = forms.CharField(
                                widget=forms.Textarea(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    achievements = forms.CharField(widget=forms.Textarea(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    future_plans = forms.CharField(widget=forms.Textarea(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    link = forms.URLField(widget=forms.Textarea(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    service_name = forms.CharField(widget=forms.Textarea(
                               attrs={'class': "input_for_form",
                                      'type': "text",
                                      }),
                           required=True)

    institute = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input_for_form",
               'type': "text",
               }),
        required=True)

    img = forms.ImageField(help_text="Фотография учёного",
                           widget=forms.FileInput(
                               attrs={'class': "input_for_form_img",
                                      'type': "file",
                                      'id': "imageInput",
                                      'name': "image",
                                      'accept': ".jpg, .jpeg, .png"}),
                           required=True)
    class Meta:
        model = Image
        fields = ['name', 'url_path', 'alt', 'lab', 'position',
                  'degree', 'teaching_info', 'scientific_interests',
                  'achievements', 'future_plans', 'link',
                  'service_name']


class CreateNewsForm(forms.Form):
    name = forms.CharField(help_text="Введите название", required=True)
    description = forms.CharField(help_text="Введите текст",
                                  widget=forms.Textarea)


class UploadDocForm(ModelForm):
    class Meta:
        model = Doc
        fields = ['name', 'category', 'path']


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
        
        doc = Doc(name=name, category='GZS')
        if commit:
            # Создаем объект Doc из documents.models и сохраняем файл
            doc.path.save(path.name, path, save=True)
            
            shc_doc = SHCDoc(doc=doc, description=description)
            shc_doc.save()
            
        return doc
