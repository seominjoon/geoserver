'''
Created on Jul 21, 2014

@author: minjoon
'''

from django.conf.urls import patterns, url

from questions import views

urlpatterns = patterns('',
    url(r'^upload/$', views.QuestionUploadView.as_view(), name='questions-upload'),
    url(r'^upload/choice$', views.ChoiceUploadView.as_view(), name='questions-upload-choice'),
    url(r'^list/(?P<query>[\w+]+)/$', views.QuestionListView.as_view(), name='questions-list'),
    url(r'^delete/(?P<slug>\d+)/$', views.QuestionDeleteView.as_view(), name='questions-delete'),
    url(r'^download/(?P<query>[\w+]+)/$', views.QuestionDownloadView.as_view(), name='questions-download'),
    url(r'^update/all/$', views.QuestionUpdateAllView.as_view(), name='questions-update_all'),
    url(r'^update/(?P<slug>\d+)/$', views.QuestionUpdateView.as_view(), name='questions-update'),
    url(r'^detail/(?P<slug>\d+)/$', views.QuestionDetailView.as_view(), name='questions-detail'),
    url(r'^createtag/$', views.TagCreateView.as_view(), name='questions-tagcreate'),
)