"""
$Date $
$Revision $
$Author $

Provides functionality for all front end requests regarding tools.
"""

import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed


"""
	Creates a new Tool and saves it to the database.
"""
def createNewTool(name, description, ownerObj, location, picture, isAvailable, \
					preferences, tags):
	toolObject = Tool()
	toolObject.name = name
	toolObject.description = description
	toolObject.tags = tags
	toolObject.owner = ownerObj
	toolObject.location = location
	toolObject.isAvailable = isAvailable
	toolObject.preferences = preferences
	toolObject.save()
	return toolObject


"""
	Get the name of a tool.
"""
def getToolName(tool):
	return tool.name


"""
	Get the description of a tool.
"""
def getToolDescription(tool):
	return tool.description


"""
	Return a list of every single tool in the database
	regardless of which shed it is in.
"""
def listAllTools():
	return Tool.objects.all()


"""
	Return a list of every tool in a specific shed.
"""
def listAllToolsInShed(shedID):
	return Tool.objects.filter(myShed=shedID)


"""
	Return a list of every available tool in a specific shed.
"""
def	listAllAvailToolsInShed(shedID):
	return Tool.objects.filter(myShed=shedID, isAvailable=1)


"""
	Return a list of all tools owned by a specific person.
"""
def listAllToolsOwnedBy(profileID):
	return Tool.objects.filter(owner=profileID)


"""
	Return a list of all tools being borrowed by a specific person.
"""
def listAllToolsBorrowedBy(profileID):
	return Tool.objects.filter(borrower=profileID)


"""
	Return a list of all tools in a shed, sorted from most borrowed to least borrowed.
"""
def listMostBorrowedToolsInShed(shedID):
	allTools = Tool.objects.all()
	for i in range(1, len(allTools)):
		val = allTools[i].borrowedCount
		j = i - 1
		while (j >= 0) and (allTools[j].borrowedCount < val):
		    allTools[j+1] = allTools[j]
		    j = j - 1
		allTools[j+1] = val
	return allTools


"""
	Return a list of all tools in a shed, sorted from most requested to least requested.
"""
def listMostRequestedToolsInShed(shedID):
	allTools = Tool.objects.all()
	for i in range(1, len(allTools)):
		val = allTools[i].requestedCount
		j = i - 1
		while (j >= 0) and (allTools[j].requestedCount < val):
		    allTools[j+1] = allTools[j]
		    j = j - 1
		allTools[j+1] = val
	return allTools
