from django.urls import path
from . import views

urlpatterns = [
    path('account/create_grant', views.create_new_grant, name='create_grant'),
    path('account', views.profile, name='profile'),
    path('account/news', views.news, name='news'),
    path('account/moder_guests', views.moder_guests, name='moder_guests'),
    path('account/gzs', views.gzs, name='gzs'),
    path('account/add_new_guests', views.add_new_guests, name='add_new_guests')
]
