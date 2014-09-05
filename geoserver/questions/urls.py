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
    url(r'^download/(?P<query>\w+)/$', views.QuestionDownloadView.as_view(), name='download'),
    url(r'^update/all/$', views.QuestionUpdateAllView.as_view(), name='update_all'),
    url(r'^update/(?P<slug>\d+)/$', views.QuestionUpdateView.as_view(), name='update'),
    url(r'^detail/(?P<slug>\d+)/$', views.QuestionDetailView.as_view(), name='detail'),
)