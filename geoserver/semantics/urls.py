from django.conf.urls import patterns, url
from semantics import views

__author__ = 'minjoon'


urlpatterns = patterns('',
                       url(r'^annotate/(?P<question_pk>\d+)/(?P<sentence_index>\d+)/$', views.SentenceParseAnnotateView.as_view(), name='semantics-annotate'),
                       url(r'^download/(?P<query>\w+)/$', views.SemanticParseDownloadView.as_view(), name='semantics-download'),
                       # url(r'^detail/(?P<slug>\d+)/$', views.LabelDetailView.as_view(), name='labels-detail'),
)
