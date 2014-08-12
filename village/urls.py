from django.conf.urls import patterns, url
from village import views

urlpatterns = patterns('',
    url(r'^$', views.overview, name='overview'),
    url(r'^upgrade/(?P<building_id>\d+)/$', views.upgrade, name='upgrade'),
    url(
    	r'^downgrade/(?P<building_id>\d+)/$', views.downgrade, name='downgrade'
    	),
)