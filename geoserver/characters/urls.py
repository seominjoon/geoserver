'''
Created on Sep 5, 2014

@author: minjoon
'''

from django.conf.urls import patterns, url

from characters import views


urlpatterns = patterns('',
    url(r'^list/$', views.CharacterListView.as_view(), name='characters-list'),
    url(r'^upload/$', views.CharacterUploadView.as_view(), name='characters-upload'),
    url(r'^update/(?P<query>\w+)/$', views.CharacterUpdateView.as_view(), name='characters-update'),
    url(r'^detail/(?P<slug>\d+)/$', views.CharacterDetailView.as_view(), name='characters-detail'),
    url(r'^delete/(?P<slug>\d+)/$', views.CharacterDeleteView.as_view(), name='characters-delete'),
)