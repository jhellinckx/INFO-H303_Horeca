from django.conf.urls import include, url
from . import views

urlpatterns = [
	#url(r'^$', views.index_requests, name="index_requests"),
	# ex: /requests/establishments/4
    #url(r'^establishments/(?P<request_id>[0-9]+)/$', views.establishments_request_detail, name='establishment_request_detail'),
    #url(r'^users/(?P<request_id>[0-9]+)/$', views.users_request_detail, name='users_request_detail'),
]