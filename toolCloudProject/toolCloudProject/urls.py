from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$','toolCloudApp.views.home', name="home"),
    url(r'^admin/', include(admin.site.urls)),


	url(r'^accounts/register/$', 'toolCloudApp.views.user_register'),
	#url(r'^accounts/tool_submission/$', 'toolCloudApp.views.tool_submission'),

    # Accounts urls
	url(r'^accounts/login/$', 'toolCloudProject.views.login'),
	url(r'^accounts/logout/$', 'toolCloudProject.views.logout'),
	url(r'^accounts/auth/$', 'toolCloudProject.views.auth_view'),
	url(r'^accounts/loggedin/$', 'toolCloudProject.views.loggedin'),
	url(r'^accounts/invalid/$', 'toolCloudProject.views.invalid_login'),
	url(r'^accounts/profile/(?P<username>\w+)/$', 'toolCloudApp.views.view_profile', name="profile"), 
	url(r'^accounts/profile/$', 'toolCloudApp.views.view_current_profile'), #current user profile, redirect to URL above
	
	# Tool urls
	url(r'^tools/$', 'toolCloudApp.views.all_tools'),
	url(r'^tools/submit/$', 'toolCloudApp.views.tool_submission'),
	url(r'^tools/toolnotfound/$', 'toolCloudApp.views.tool_dne'),
	url(r'^tools/(?P<id>\d+)/$', 'toolCloudApp.views.view_tool_page', name="toolPage"),

	#Shed urls
	url(r'^shed/shedCreation', 'toolCloudApp.views.create_toolShed'),
	
	# sekret
	url(r'^3spooky5me/$', 'toolCloudApp.views.spooked'),
	url(r'^aspookedeh/$', 'toolCloudApp.views.spooky')
)