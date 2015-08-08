from django.conf.urls import patterns, url
from semantics import views

__author__ = 'minjoon'


urlpatterns = patterns('',
                       url(r'^annotate/(?P<question_pk>\d+)/(?P<sentence_index>\d+)/$', views.SentenceParseAnnotateView.as_view(), name='semantics-annotate'),
                       url(r'^download/(?P<query>[\w+]+)/$', views.SemanticParseDownloadView.as_view(), name='semantics-download'),
                       url(r'^list/(?P<query>[\w+]+)/$', views.SemanticParseListView.as_view(), name='semantics-list'),
                       url(r'^annotate/(?P<question_pk>\d+)/(?P<choice_number>\d+)/$', views.ChoiceAnnotateView.as_view(), name='semantics-choice-annotate'),
                       # url(r'^detail/(?P<slug>\d+)/$', views.LabelDetailView.as_view(), name='labels-detail'),
)
