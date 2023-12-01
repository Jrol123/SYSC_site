from django.urls import path
from . import views

urlpatterns = [
    path('account/create_user', views.create_new_user, name='create_user'),
    path('account/create_institute', views.create_new_institute, name='create_institute'),
]
