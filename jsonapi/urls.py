from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^germplasm/(?P<pk>[^ /]+)/$', views.germplasm_details),
    url(r'^germplasm/(?P<pk>[^ /]+)/$', views.germplasm_details),
]
