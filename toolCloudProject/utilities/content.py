#!/usr/bin/env python

import sys
import utilities.profileUtilities as profileUtil
import utilities.shedUtilities as shedUtil
import utilities.toolUtilities as toolUtil
import utilities.notificationUtilities as notifUtil

"""
	Build content dict using other utilities (deprecated - TO BE DELETED)
"""
#def genContent(request):
#	if request.user.is_anonymous():#no special changes of content
#		return defaults
#	custom = defaults.copy()
#	name = request.user.username
#	replace(custom, 'name', name)
#	custom['first_name']=request.user.first_name
#	custom['last_name']=request.user.last_name
#	profile = profileUtil.getProfileFromUser(request.user)
#	custom['address']=profileUtil.getAddress(profile)
#	return custom
"""
	Header - String
	Footer - String
	copyrightYear - String
	company - String
"""
def genSuper():
	return {'heading' : "ToolCloud",
			'footer'  : "made with <3 from the squad",
	'copyrightYear'	  : "2014",
			'company' : "Investiny Corp."}

"""
	adds the clever phrases for below the loggedOut header
"""
def addSubTitleStrings(contentDict):
    file = open("homePageText.txt","r")
    strings = file.readlines()
    contentDict['strings'] = strings
    return contentDict

"""
	adds a failed login notification to the dict and returns it
"""
def addFailedLoginNoti(contentDict):
	newNoti = notifUtil.createTempInfoNotif("Login failed. D:"
					+ " Please check your username and password and try again.", "alert")
	return addNoti(contentDict, newNoti)

"""
	adds a sucessful login notification to the dict and returns it
"""
def addGoodLoginNoti(contentDict):
	newNoti = notifUtil.createTempInfoNotif("Login sucessful! :D", "success")
	return addNoti(contentDict, newNoti)

"""
	adds a sucessful registration notification to the dict and returns it
"""
def addGoodRegisterNoti(contentDict):
	newNoti = notifUtil.createTempInfoNotif("Registration sucessful! You are now logged in.", "success")
	return addNoti(contentDict, newNoti)

"""
	adds a sucessful logout notification to the dict and returns it
"""
def addGoodLogoutNoti(contentDict):
	newNoti = notifUtil.createTempInfoNotif("Logout sucessful. Have a good day. :)", "success")
	return addNoti(contentDict, newNoti)

"""
	adds the passed notification to the passed dict, abiding by django content dict standard
"""
def addNoti(contentDict, notification):
	if 'desktopNotifs' in contentDict and contentDict['desktopNotifs'] is not None:#exists, needs to be added to list
		contentDict['desktopNotifs'] += notification
		return contentDict
	#does not exist yet, so we need to add it in an array
	contentDict['desktopNotifs'] = [notification]
	return contentDict

"""
	username - String
	first_name - String
	last_name - String
	picture - String
	topSheds - object[]
	notifications - object[]
"""
def genBaseLoggedIn(request):
	results = dict()
	results.update(genSuper())
	results['username'] = request.user.username
	results['first_name'] = request.user.first_name
	results['last_name'] = request.user.last_name
	#get pict location
	results['picture'] = None
	#get top sheds
	results['topSheds'] = None
	#get notifications
	results.update(getNotifications(request))
	return results

"""
	tools - object (name, status, desc, pict, borrowcount,
					requestcount, location)
	sheds - object (name, location, numOfUsers, privacy level,
					sharezone, minRepuation)
	community - object (map code, list of sheds, numOfToolsOut,
					numOfToolsTotal)
	toolsBorrowed - object (array of tool objects)
			each as (name, time left, time borrowed, timestamp)
"""
def genUserHome(request):
	results = genBaseLoggedIn(request)
	profile = profileUtil.getProfileFromUser(request.user)
	tools = toolUtil.getAllToolsOwnedBy(profile)
	sheds = shedUtil.getAllShedsJoinedBy(profile)
	#sheds = None
	borrowedTools = toolUtil.getAllToolsBorrowedBy(profile)
	#borrowedTools = None
	#print(profile)
	#results['notif'] = notifUtil.getAllActiveProfileNotifs(profile)
	sharezone = profileUtil.getSharezone(profile)
	sharezoneMembers = profileUtil.getAllProfilesInSharezone(sharezone)
	#not done
	results['tools'] = tools
	results['sheds'] = sheds
	results['borrowed'] = borrowedTools
	results['sharezone'] = sharezone
	results['sharezoneMembers'] = sharezoneMembers
	return results

def genJustRegistered(account, profile):
	results = genSuper()
	results['username'] = account.username
	results['first_name'] = account.first_name
	results['last_name'] = account.last_name
	results['picture'] = None
	results['topSheds'] = None
	sheds = shedUtil.getAllShedsJoinedBy(profile)
	sharezone = profileUtil.getSharezone(profile)
	sharezoneMembers = profileUtil.getAllProfilesInSharezone(sharezone)
	#not done
	results['tools'] = None
	results['sheds'] = sheds
	results['borrowed'] = None
	results['sharezone'] = sharezone
	results['sharezoneMembers'] = sharezoneMembers
	return addGoodRegisterNoti(results)

def genLogin(request):
	return genSuper()

def genViewNotifications(request):
	content = genBaseLoggedIn(request)
	content.update(getNotifications(request))
	return content

#BEGIN UTILITY FUNCTIONS

def getNotifications(request):#returns a dict with the userProfile and notifs values filled
	if request.user.is_anonymous():#anon no notis
		return None
	userProfile = profileUtil.getProfileFromUser(request.user)
	notifs = notifUtil.getAllActiveProfileNotifs(userProfile)
	context = {}
	context['currentUserProfile'] = userProfile
	context['notifs'] = notifs
	return context

def replace(dictionary, key, newValue):
	for k in dictionary.keys():
		if k == key:
			dictionary[key] = newValue
