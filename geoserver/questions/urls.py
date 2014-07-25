'''
Created on Jul 21, 2014

@author: minjoon
'''

from django.conf.urls import patterns, url

from questions import views

urlpatterns = patterns('',
    url(r'^upload/$', views.QuestionUploadView.as_view(), name='upload'),
    url(r'^list/$', views.QuestionListView.as_view(), name='list'),
    url(r'^delete/(?P<slug>\d+)/$', views.QuestionDeleteView.as_view(), name='delete'),
    url(r'^download/(?P<query>\w+)/$', views.QuestionDownloadView.as_view(), name='download')
)