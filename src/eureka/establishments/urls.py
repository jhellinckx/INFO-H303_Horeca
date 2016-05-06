from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	# ex: /establishments/restaurant/5
    url(r'^restaurant/(?P<establishment_id>[0-9]+)/$', views.restaurant_detail, name='restaurant_detail'),
    url(r'^bar/(?P<establishment_id>[0-9]+)/$', views.bar_detail, name='bar_detail'),
    url(r'^hotel/(?P<establishment_id>[0-9]+)/$', views.hotel_detail, name='hotel_detail'),
    url(r'^search/$', views.results, name="results"),
]