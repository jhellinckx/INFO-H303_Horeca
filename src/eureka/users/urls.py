from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^(?P<username>[\w.@+-]+)/$', views.user_detail,name="user_detail"),
]