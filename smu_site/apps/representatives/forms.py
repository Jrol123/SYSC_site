from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from documents.models import Doc
from info.models import Institute
from news.models import Image


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
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': "input_for_form",
               'type': "text",
               'placeholder': "Введите ФИО учёного"}),
        required=True)
    
    path = forms.FileField(
        help_text='Загрузить документ',
        widget=forms.FileInput(attrs={
            'class': "input_for_form_img",
            'type': "file",
            'accept': ".doc, .docx, .xls, .txt, .rtf, .pdf",
            'id': "documentUpload", 'name': "documentUpload"}),
        required=True)
    
    category = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': "input_for_form",
            'type': "text"}),
        required=True)
    
    class Meta:
        model = Doc
        fields = ['name', 'category', 'path']
    
    # def save(self, commit=True):
    #     name = self.cleaned_data['name']
    #     path = self.cleaned_data['path']
    #     description = self.cleaned_data['description']
    #
    #     doc = Doc(name=name, category='GZS')
    #     if commit:
    #         # Создаем объект Doc из documents.models и сохраняем файл
    #         doc.path.save(path.name, path, save=True)
    #
    #         shc_doc = SHCDoc(doc=doc, description=description)
    #         shc_doc.save()
    #
    #     return doc
