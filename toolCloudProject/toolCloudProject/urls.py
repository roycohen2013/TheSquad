from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','toolCloudApp.views.home', name="home"),
    url(r'^admin/', include(admin.site.urls)),


	url(r'^accounts/register/$', 'toolCloudApp.views.user_register'),

    # Accounts urls
	url(r'^accounts/login/$', 'toolCloudProject.views.login'),
	url(r'^accounts/logout/$', 'toolCloudProject.views.logout'),
	url(r'^accounts/auth/$', 'toolCloudProject.views.auth_view'),
	url(r'^accounts/loggedin/$', 'toolCloudProject.views.loggedin'),
	url(r'^accounts/invalid/$', 'toolCloudProject.views.invalid_login'),


	# Tool urls
	#url(r'^tools/submit/$', 'toolCloudApp.views.tool_submission')
)