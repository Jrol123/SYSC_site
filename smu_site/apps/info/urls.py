from django.urls import path
from . import views


app_name = 'info'

urlpatterns = [
    path('organization/', views.organization, name='organization'),
    path('institutes/', views.institutes, name='institutes'),
    path('grant/', views.grant, name='grant'),
    path('institutes/<int:inst_id>/', views.institute_info,
         name='institute_info')
]
