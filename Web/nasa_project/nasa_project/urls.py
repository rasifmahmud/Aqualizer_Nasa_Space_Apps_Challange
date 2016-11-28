from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'api.views.login'),
	url(r'^accounts/login/$', 'api.views.login'),
	url(r'^accounts/edit/$', 'api.views.edit'),
	url(r'^accounts/guest_page/$', 'api.views.guest_page'),
	url(r'^accounts/guest_page/(?P<geo>.+)$', 'api.views.geo_detail'),
	url(r'^accounts/loading_main_page/$', 'api.views.loading_main_page'),
	url(r'^accounts/loading_login_page/$', 'api.views.loading_login_page'),
	url(r'^accounts/auth/$', 'api.views.auth_view'),
	url(r'^accounts/logout/$', 'api.views.logout'),
	url(r'^accounts/loggedin/$', 'api.views.loggedin'),
	url(r'^accounts/invalid/$', 'api.views.invalid_login'),
	url(r'^accounts/register/$', 'api.views.register_user'),
	url(r'^accounts/register_success/$', 'api.views.register_success'),
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
