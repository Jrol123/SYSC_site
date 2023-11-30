from django.urls import path
from . import views

urlpatterns = [
    path('account/create_user', views.create_new_user, name='create_user'),
]
