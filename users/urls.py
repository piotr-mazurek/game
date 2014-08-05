from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns(
    '',
    url(r'^login/', views.authenticate_user, name='login'),
    url(r'^login_show/', views.login_show, name='login_show'),
    url(r'^$', views.login_show),
    # url(r'^logout/', views.logout),
    # url(r'^register/', views.register),
    url(r'^profile/', views.profile, name='profile'),
    # url(r'^profile/edit/', views.edit),
)
