from django.conf.urls import patterns, url
from village import views

urlpatterns = patterns(
    '',
    url(r'^$', views.overview, name='overview'),
    url(r'^upgrade/(?P<building_id>\d+)/$', views.upgrade, name='upgrade'),
    url(
        r'^downgrade/(?P<building_id>\d+)/$', views.downgrade, name='downgrade'
    ),
    url(
        r'^building/(?P<id>\d+)/$',
        views.building_detail,
        name='building_detail'
    ),
    url(
        r'^village_name_change/(?P<village_id>\d+)$',
        views.village_name_change,
        name='village_name_change'
    )
)
