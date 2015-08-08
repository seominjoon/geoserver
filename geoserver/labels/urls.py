from django.conf.urls import patterns, url
from labels import views

__author__ = 'minjoon'


urlpatterns = patterns('',
    url(r'^create/(?P<slug>\d+)/$', views.LabelCreateView.as_view(), name='labels-create'),
    url(r'^list/(?P<query>[\w+]+)/$', views.LabelListView.as_view(), name='labels-list'),
    url(r'^download/(?P<query>[\w+]+)/$', views.LabelDownloadView.as_view(), name='labels-download'),
    url(r'^delete/(?P<slug>\d+)/$', views.LabelDeleteView.as_view(), name='labels-delete'),
    url(r'^detail/(?P<slug>\d+)/$', views.LabelDetailView.as_view(), name='labels-detail'),
)
