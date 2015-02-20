from django.conf.urls import patterns, url
from semantics import views

__author__ = 'minjoon'


urlpatterns = patterns('',
                       url(r'^create/(?P<slug>\d+)/$', views.SemanticParseCreateView.as_view(), name='semantic-parses-create'),
                       url(r'^list/$', views.SemanticParseListView.as_view(), name='semantic-parses-list'),
                       url(r'^download/(?P<query>\w+)/$', views.SemanticParseDownloadView.as_view(), name='semantic-parses-download'),
                       # url(r'^detail/(?P<slug>\d+)/$', views.LabelDetailView.as_view(), name='labels-detail'),
)
