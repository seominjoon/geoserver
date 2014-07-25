'''
Created on Jul 21, 2014

@author: minjoon
'''

from django.conf.urls import patterns, url

from deptrees import views


urlpatterns = patterns('',
    url(r'^upload/$', views.DepTreeUploadView.as_view(), name='upload'),
    url(r'^list/$', views.DepTreeListView.as_view(), name='list'),
)