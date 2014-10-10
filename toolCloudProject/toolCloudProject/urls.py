from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','toolCloudApp.views.home', name="home"),
    url(r'^admin/', include(admin.site.urls)),
    # Accounts urls
	url(r'^accounts/login/$', 'toolCloudApp.views.user_login'),
	url(r'^accounts/logout/$', 'toolCloudApp.views.user_logout'),
	url(r'^accounts/register/$', 'toolCloudApp.views.user_register'),
	# Tool urls
	#url(r'^tools/submit/$', 'toolCloudApp.views.tool_submission')
)