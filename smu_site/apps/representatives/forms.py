from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.db import connection
from documents.models import Doc, Category
from info.models import Institute
from news.models import Image


class CreateScientistForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs=
                               {'class': "input_for_form",
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

    scientific_interests = forms.CharField(
        widget=forms.Textarea(
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

    class Meta:
        model = Image
        fields = ['name', 'url_path', 'alt', 'lab', 'position',
                  'degree', 'scientific_interests',
                  'link', 'service_name']
        widgets = {'url_path': forms.FileInput(
            attrs={'class': "input_for_form_img",
                   'type': "file",
                   'id': "imageInput",
                   'name': "image",
                   'accept': ".jpg, .jpeg, .png"})}


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
