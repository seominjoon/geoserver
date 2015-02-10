from django.conf.urls import patterns, url
from labels import views

__author__ = 'minjoon'


urlpatterns = patterns('',
    url(r'^create/(?P<slug>\d+)/$', views.LabelCreateView.as_view(), name='labels-create'),
    url(r'^list/$', views.LabelListView.as_view(), name='labels-list'),
    # url(r'^detail/(?P<slug>\d+)/$', views.LabelDetailView.as_view(), name='labels-detail'),
)
