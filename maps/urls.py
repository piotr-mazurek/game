from django.conf.urls import patterns, url
from characters import views

urlpatterns = patterns(
    '',
    url(r'^map/$', views.map, name='map'),
    )
