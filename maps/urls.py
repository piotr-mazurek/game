from django.conf.urls import patterns, url
from maps import views

urlpatterns = patterns(
    '',
    url(r'^$', views.map_view, name='map_view'),
    url(r'^visual$', views.map_view, name='visual'),
    url(r'^init$', views.init_db_map, name='init_db_map'),
    )
