from django.conf.urls import patterns, url
from rest_framework.authtoken import views

urlpatterns = patterns(
    'api.views',
    url(r'^water/(?P<data>.+)$', 'water_list', name='water_list'),
    url(r'^water/$', 'get_water', name='get_water'),
)
