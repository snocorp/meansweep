from django.conf.urls import patterns, url

from minesweep import views

urlpatterns = patterns('',
    url(r'^(?P<field_id>\d+)/$', views.field, name='field'),
    url(r'^flag/(?P<field_id>\d+)/(?P<x>\d+)/(?P<y>\d+)$', views.flag, name='flag'),
    url(r'^sweep/(?P<field_id>\d+)/(?P<x>\d+)/(?P<y>\d+)$', views.sweep, name='sweep'),
    url(r'^new/(?P<width>\d+)/(?P<height>\d+)/(?P<chance>\d+)$', views.new, name='new')
)