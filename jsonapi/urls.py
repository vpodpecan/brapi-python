from django.conf.urls import url, include

from jsonapi import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
    url(r'^calls$', views.CallSearch.as_view()),
    url(r'^germplasm/(?P<germplasmDbId>[^ /]+)$', views.GermplasmDetails.as_view()),
    url(r'^germplasm-search$', views.GermplasmSearch.as_view()),
    url(r'^programs$', views.ProgramList.as_view()),
    url(r'^trials/(?P<trialDbId>[^ /]+)$', views.TrialDetails.as_view()),
    url(r'^trials$', views.TrialList.as_view()),
    url(r'^studies$', views.StudyList.as_view()),
    url(r'^studies/(?P<studyDbId>[^ /]+)$', views.StudyDetails.as_view()),
    url(r'^studies-search$', views.StudySearch.as_view()),
    url(r'^studies/(?P<studyDbId>[^ /]+)/observationVariables$', views.StudyObservationVariable.as_view()),
    url(r'^studies/(?P<studyDbId>[^ /]+)/germplasm$', views.StudyGermplasm.as_view()),
]
