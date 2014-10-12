#!/usr/bin/env python

import sys
import utilities.profileUtilities as profileUtil
import utilities.extraUtilities as extraUtil
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
	return custom

def getDefaults():
	return defaults

def replace(dictionary, key, newValue):
	for k in dictionary.keys():
		if k == key:
			dictionary[key] = newValue
