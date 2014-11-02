'''
Created on Jul 21, 2014

@author: minjoon
'''

from django.conf.urls import patterns, url

from deptrees import views


urlpatterns = patterns('',
    url(r'^upload/$', views.DepTreeUploadView.as_view(), name='deptrees-upload'),
    url(r'^list/$', views.DepTreeListView.as_view(), name='deptrees-list'),
    url(r'^upload/image/$', views.DepTreeImageUploadView.as_view(), name='deptrees-upload_image'),
    url(r'^demo/$', views.DepTreeDemoView.as_view(), name='deptrees-demo'),
    url(r'^detail/(?P<slug>\d+)/$', views.DepTreeDetailView.as_view(), name='deptrees-detail'),
)