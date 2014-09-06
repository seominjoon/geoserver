from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'geoserver.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^characters/', include('characters.urls')),
    url(r'^questions/', include('questions.urls')),
    url(r'^deptrees/', include('deptrees.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
