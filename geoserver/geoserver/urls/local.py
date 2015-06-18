from django.conf.urls import patterns, include, url

from django.contrib import admin
from geoserver import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geoserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^semantics/', include('semantics.urls')),
    url(r'^labels/', include('labels.urls')),
    url(r'^questions/', include('questions.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.local.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.local.MEDIA_ROOT, }),
        url(r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.local.STATIC_ROOT, }),
    )
