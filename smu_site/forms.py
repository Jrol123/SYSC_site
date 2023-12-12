from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Имя пользователя",
        'required': "",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id': "myInput",
        'placeholder': "пароль",
        'required': "",
    }))

    def clean_password(self):
        cd = self.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password'])
        if user is None:
            raise ValidationError('')
        return cd['password']

    def clean_username(self):
        cd = self.cleaned_data
        return cd['username']
