'''
Created on Jul 21, 2014

@author: minjoon
'''

from django.conf.urls import patterns, url

from ocrs import views

urlpatterns = patterns('',
    url(r'^upload/$', views.OCRUploadView.as_view(), name='ocrs-upload'),
    url(r'^download/(?P<pk>\d+)/$', views.OCRDownloadView.as_view(), name='ocrs-download'),
    url(r'^test/$', views.OCRTestView.as_view(), name='ocrs-test'),
)