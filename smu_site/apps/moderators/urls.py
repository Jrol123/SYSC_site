from django.urls import path
from . import views

urlpatterns = [
    path('account/create_user', views.create_new_user, name='create_user'),
    path('account/create_grant', views.create_new_grant, name='create_grant'),
]
