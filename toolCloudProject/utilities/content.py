#!/usr/bin/env python

import sys
import utilities.profileUtilities as profileUtil
import utilities.shedUtilities as shedUtil
import utilities.toolUtilities as toolUtil

defaults = {
	'heading' : "ToolCloud",
	'name' : "Anonymous"
}

"""
	Build content dict using other utilities
"""
def genContent(request):
	if request.user.is_anonymous():#no special changes of content
		return defaults
	custom = defaults.copy()
	name = request.user.username
	replace(custom, 'name', name)
	custom['first_name']=request.user.first_name
	custom['last_name']=request.user.last_name
	profile = profileUtil.getProfileFromUser(request.user)
	custom['address']=profileUtil.getAddress(profile)
	return custom
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
	results['notifications'] = None
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
	results = dict()
	results.update(genBaseLoggedIn(request))
	profile = profileUtil.getProfileFromUser(request.user)
	tools = toolUtil.getAllToolsOwnedBy(profile)
	sheds = shedUtil.getAllShedsJoinedBy(profile)
	#sheds = None
	borrowedTools = toolUtil.getAllToolsBorrowedBy(profile)
	#borrowedTools = None
	#print(profile)
	sharezone = profileUtil.getSharezone(profile)
	sharezoneMembers = profileUtil.getAllProfilesInSharezone(sharezone)
	#not done
	results['tools'] = tools
	results['sheds'] = sheds
	results['borrowed'] = borrowedTools
	results['sharezone'] = sharezone
	results['sharezoneMembers'] = sharezoneMembers
	return results

def getDefaults():
	return defaults

def replace(dictionary, key, newValue):
	for k in dictionary.keys():
		if k == key:
			dictionary[key] = newValue
