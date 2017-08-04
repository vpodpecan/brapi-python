from django.conf.urls import url, include

from jsonapi import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
    url(r'^germplasm/(?P<germplasmDbId>[^ /]+)/$', views.GermplasmDetails.as_view()),
    url(r'^germplasm-search/$', views.GermplasmSearch.as_view()),
    url(r'^programs/$', views.ProgramList.as_view()),
    url(r'^trials/(?P<trialDbId>[^ /]+)/$', views.TrialDetails.as_view()),

]
