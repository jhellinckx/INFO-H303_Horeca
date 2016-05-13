from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^create_restaurant/', views.create_restaurant, name="create_restaurant"),
	url(r'^create_bar/', views.create_bar, name="create_bar"),
	url(r'^create_hotel/', views.create_hotel, name="create_hotel"),
	url(r'^create_user/', views.create_user, name="create_user"),
]

urlpatterns += staticfiles_urlpatterns()