from django.urls import path
from . import views


app_name = 'info'

urlpatterns = [
    path('institutes/', views.institutes, name='institutes'),
    path('grant/', views.grant, name='grant')
]
