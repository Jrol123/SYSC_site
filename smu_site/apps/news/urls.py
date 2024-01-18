from django.urls import path
from . import views


app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:news_id>/', views.newspage, name='newspage'),
    path('events/<int:event_id>/', views.eventpage, name='eventpage'),
]
