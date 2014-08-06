from django.conf.urls import patterns, url
from characters import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^(?P<character_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<character_id>\d+)/delete$', views.delete, name='delete'),
    )