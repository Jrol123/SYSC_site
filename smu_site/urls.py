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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views, settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='main'),
    path('news/', include('news.urls'), name='news'),
    path('documents/', include('documents.urls')),
    path('info/', include('info.urls')),
    path('moderators/', include('moderators.urls')),
    path('accounts/login', include('django.contrib.auth.urls')),
    path('accounts/login', views.user_login, name='user_login'),
    # path('representatives/', include(
    #      ('representatives.urls', 'representatives'),
    #      namespace='representatives')),
    path('representatives/', include('representatives.urls')),
    path('SHC/', include('SHC.urls')),
    path('delete/<str:obj_type>/<int:id>', views.readelete, name='delete_news'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
