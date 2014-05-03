from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    url(r'^meansweep/', include('minesweep.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
