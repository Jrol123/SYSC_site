"""
URL configuration for smu_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('documents/', include('documents.urls')),
    path('info/', include('info.urls')),
    # path('moderators/', include(('moderators.urls', 'moderators'),
    #                             namespace='moderators')),
    path('news/', include('news.urls')),
    # path('representatives/', include(
    #     ('representatives.urls', 'representatives'),
    #     namespace='representatives')),
    # path('SHC/', include(('SHC.urls', 'SHC'), namespace='SHC'))
]
