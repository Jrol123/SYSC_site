from django.urls import path
from . import views

app_name = 'moderators'

urlpatterns = [
    path('account/create_grant', views.create_new_grant, name='create_grant'),
    path('account', views.news, name='news'),
    path('account/save_news', views.save_news, name='save_news'),
    path('account/moder_guests', views.moder_guests, name='moder_guests'),
    path('account/gzs', views.gzs, name='gzs'),
    path('account/add_new_guests', views.add_new_guests, name='add_new_guests'),
    path('account/create_new_institute', views.create_new_institute, name='create_institute'),
]
