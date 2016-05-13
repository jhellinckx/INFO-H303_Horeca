from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^create_restaurant/', views.create_restaurant, name="create_restaurant"),
	url(r'^create_bar/', views.create_bar, name="create_bar"),
	url(r'^create_hotel/', views.create_hotel, name="create_hotel"),
	
	url(r'^edit_restaurant/(?P<establishment_id>[0-9]+)/$', views.edit_restaurant, name='edit_restaurant'),
	url(r'^edit_bar/(?P<establishment_id>[0-9]+)/$', views.edit_bar, name='edit_bar'),
	url(r'^edit_hotel/(?P<establishment_id>[0-9]+)/$', views.edit_hotel, name='edit_hotel'),

	url(r'^delete_restaurant/(?P<establishment_id>[0-9]+)/$', views.delete_restaurant, name='delete_restaurant'),
	url(r'^delete_bar/(?P<establishment_id>[0-9]+)/$', views.delete_bar, name='delete_bar'),
	url(r'^delete_hotel/(?P<establishment_id>[0-9]+)/$', views.delete_hotel, name='delete_hotel'),

	url(r'^create_user/', views.create_user, name="create_user"),
]

urlpatterns += staticfiles_urlpatterns()