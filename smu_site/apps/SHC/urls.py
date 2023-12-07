from django.urls import path
from . import views


app_name = "SHC"

urlpatterns = [
    path('', views.index, name='index'),
]
