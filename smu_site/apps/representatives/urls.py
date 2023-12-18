from django.urls import path
from . import views


app_name = 'representatives'

urlpatterns = [
    path('account', views.create_news, name='news'),
    path('account/save_news', views.save_news, name='save_news'),
    path('account/create_scientist', views.create_scientist, name='create_scientist'),
    # path('account/create_new_institute', views.create_new_institute, name='create_institute'),
    # path('account/create_new_grant', views.create_new_grant, name='create_new_grant'),
    path('account/upload_doc', views.upload_doc, name='upload_doc'),
    # path('<int:institute_id>/', views.create_scientist, name='index'),
]
