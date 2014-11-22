"""
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
def getToolName(toolObj):
	return toolObj.name

"""
	Get a tool object with the Tool's ID
"""
def getToolFromID(toolID):
	return Tool.objects.get(id = toolID)

"""
	Update tool name.
"""
def updateToolName(toolObj, newName):
	toolObj.name = newName
	toolObj.save()
	return toolObj


"""
	Get the description of a tool.
"""
def getToolDescription(toolObj):
	return toolObj.description


"""
	Update tool description.
"""
def updateToolDescription(toolObj, newDescription):
	toolObj.description = newDescription
	toolObj.save()
	return toolObj


"""
	Get the tags of a tool.
"""
def getToolTags(toolObj):
	return toolObj.tags


"""
	Updated the tags of a tool.
"""
def updateToolTags(toolObj, newTags):
	toolObj.tags = newTags
	toolObj.save()
	return toolObj


"""
	Get the owner of a tool.
"""
def getToolOwner(toolObj):
	return toolObj.owner


"""
	Get the borrower of a tool.
"""
def getToolBorrower(toolObj):
	return toolObj.borrower


"""
	Update the borrower of a tool.
"""
def updateToolBorrower(toolObj,profileObj):
	toolObj.borrower = profileObj
	toolObj.save()
	return toolObj


"""
	Get the shed that a tool belongs to.
"""
def getToolShed(toolObj):
	return toolObj.myShed


"""
	Update the shed a tool belongs to.
"""
def updateToolShed(toolObj, shedObj):
	toolObj.myShed = shedObj
	toolObj.save()
	return toolObj


"""
	Get the location of a tool.
"""
def getToolLocation(toolObj):
	return toolObj.location


"""
	Update the location of a tool.
"""
def updateToolLocation(toolObj, newLocation):
	toolObj.location = newLocation
	toolObj.save()
	return toolObj


"""
	Get the condition of a tool.
"""
def getToolCondition(toolObj):
	return toolObj.condition


def getToolConditionReadable(toolObj):
	return toolObj.conditionReadable

	
"""
	Update the condition of a tool.
"""
def updateToolCondition(toolObj, newCondition):
	toolObj.condition = newCondition
	toolObj.save()
	return toolObj


"""
	Get the availability (boolean value) of a tool.
"""
def isToolAvailable(toolObj):
	return toolObj.isAvailable


"""
	Update the availability (boolean value) of a tool.
"""
def updateToolAvailability(toolObj, booleanVal):
	toolObj.isAvailable = booleanVal
	toolObj.save()
	return toolObj


"""
	Get the number of times a tool has been borrowed.
"""
def getBorrowedCount(toolObj):
	return toolObj.borrowedCount


"""
	Increment the number of times a tool has been borrowed.
"""
def incrementBorrowedCount(toolObj):
	toolObj.borrowedCount = toolObj.borrowedCount + 1
	toolObj.save()
	return toolObj


"""
	Get the number of times a tool has been requested.
"""
def getRequestedCount(toolObj):
	return toolObj.requestedCount


"""
	Increment the number of times a tool has been requested.
"""
def incrementRequestedCount(toolObj):
	toolObj.requestedCount = toolObj.requestedCount + 1
	toolObj.save()
	return toolObj


"""
	Return a list of every single tool in the database
	regardless of which shed it is in.
"""
def getAllTools():
	return Tool.objects.all().order_by('name')


"""
	Return a list of every tool in a specific shed.
"""
def getAllToolsInShed(shedObj):
	return Tool.objects.filter(myShed=shedObj).order_by('name')


"""
	Return a list of every available tool in a specific shed.
"""
def getAllAvailToolsInShed(shedObj):
	return Tool.objects.filter(myShed=shedObj, isAvailable=True).order_by('name')


"""
	Return a list of all tools owned by a specific person.
"""
def getAllToolsOwnedBy(profileObj):
	return Tool.objects.filter(owner=profileObj).order_by('name')


"""
	Return a list of all tools being borrowed by a specific person.
"""
def getAllToolsBorrowedBy(profileObj):
	return Tool.objects.filter(borrower=profileObj).order_by('name')


"""
	Return a list of all tools in a shed, sorted from most borrowed to least borrowed.
"""
def getMostBorrowedToolsInShed(shedObj):
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
def getMostRequestedToolsInShed(shedObj):
	allTools = Tool.objects.all()
	for i in range(1, len(allTools)):
		val = allTools[i].requestedCount
		j = i - 1
		while (j >= 0) and (allTools[j].requestedCount < val):
		    allTools[j+1] = allTools[j]
		    j = j - 1
		allTools[j+1] = val
	return allTools
