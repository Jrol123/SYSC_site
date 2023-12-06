from django.urls import path
from . import views

urlpatterns = [
    path('account/create_user', views.create_new_user, name='create_user'),
    path('account', views.profile, name='profile'),
    path('account/news', views.news, name='news'),
    path('account/moder_guests', views.moder_guests, name='moder_guests'),
    path('account/grants', views.grants, name='grants'),
    path('account/gzs', views.gzs, name='gzs'),
    path('account/add_new_guests', views.add_new_guests, name='add_new_guests')
]
