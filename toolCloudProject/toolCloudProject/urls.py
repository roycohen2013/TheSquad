from django.conf.urls import patterns, include, url
from utilities import content

from django.contrib import admin
admin.autodiscover()
handler404 = 'toolCloudApp.views.dne'
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
	url(r'^accounts/my_account/$', 'toolCloudApp.views.view_current_profile'),

	# Notification urls
	url(r'^accounts/notifications/$', 'toolCloudApp.views.view_notifications'),
	url(r'^accounts/notifications/(?P<id>\d+)/request_accept/$', 'toolCloudApp.views.request_accept'),
	url(r'^accounts/notifications/(?P<id>\d+)/request_decline/$', 'toolCloudApp.views.request_decline'),

	# Tool urls
	url(r'^tools/$', 'toolCloudApp.views.all_tools'),
	url(r'^tools/submit/$', 'toolCloudApp.views.tool_submission'),
	url(r'^tools/(?P<id>\d+)/$', 'toolCloudApp.views.view_tool_page', {'contextArg': None}, name="toolPage"),
	url(r'^tools/(?P<id>\d+)/borrow/$', 'toolCloudApp.views.borrow_tool', name="borrowRequest"),
	url(r'^tools/(?P<id>\d+)/return/$', 'toolCloudApp.views.return_tool', name="toolReturn"),
	url(r'^tools/(?P<id>\d+)/returned/$', 'toolCloudApp.views.view_tool_page', \
		{'contextArg': content.addToolReturnedNoti(dict())}, name="toolReturned"),
	url(r'^tools/(?P<id>\d+)/edit/$', 'toolCloudApp.views.edit_tool', name="toolEdit"),
	url(r'^tools/(?P<id>\d+)/request_sent/$', 'toolCloudApp.views.view_tool_page', \
		{'contextArg': content.addBorrowRequestNoti(dict())}),

	# Shed urls
	url(r'^sheds/$', 'toolCloudApp.views.all_sheds'),
	url(r'^sheds/create/$', 'toolCloudApp.views.create_tool_shed'),
	url(r'^sheds/(?P<id>\d+)/$', 'toolCloudApp.views.view_shed_page', {'contextArg': None}, name="shedPage"),
	url(r'^sheds/(?P<id>\d+)/join/$', 'toolCloudApp.views.join_shed', name="joinRequest"),
	url(r'^sheds/(?P<id>\d+)/edit/$', 'toolCloudApp.views.edit_shed', name="shedEdit"),
	url(r'^sheds/(?P<id>\d+)/request_sent/$', 'toolCloudApp.views.view_shed_page', \
		{'contextArg': content.addShedJoinRequestNoti(dict())}),

	# Community urls
	url(r'^communities/(?P<sharezone>\d+)/$', 'toolCloudApp.views.view_community_page', name="communityPage"),

	# misc
	url(r'^about_us/$', 'toolCloudApp.views.about_us'),

	# sekret
	url(r'^3spooky5me/$', 'toolCloudApp.views.spooked'),
	url(r'^aspookedeh/$', 'toolCloudApp.views.spooky'),
	
	url(r'^debug/$', 'toolCloudApp.admin.debug')
)