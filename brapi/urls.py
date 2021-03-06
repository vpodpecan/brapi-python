"""brapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from pages.views import home

urlpatterns = [
    url(r'^$', home),
    url(r'^brapi/v1/', include('jsonapi.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^iprestrict/', include('iprestrict.urls', namespace='iprestrict')),

    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
