"""
	Provides functionality for all Action objects.
	(tool borrowing and shed requests)
"""

import utilities.actionManager
import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed,Notification,Action


"""
	forces processing of actions
"""
def forceProcessActions():
	utilities.actionManager.processActions()

"""
	Will be called by the UI when a person hits the button
	to request to borrow a tool. This will create an action object 
	with a currentState equal to "userBorrowRequest" which will be processed
	by the actionManager.py ultimately sending a notification to the 
	owner of the tool and what not.
"""
def createBorrowRequestAction(tool,requester):
	newAction = Action(tool=tool,requester = requester,actionType="tool",currrentState = "userBorrowRequest")
	newAction.save()
	utilities.actionManager.processActions()
	return newAction


"""
	Creates a new Action object for a Profile requesting to join a Shed.
	The currentState field for the object is set to "userShedRequest"
"""
def createShedRequestAction(shed,requester):
	newAction = Action(shed=shed,requester = requester,actionType="shed",currrentState= "userShedRequest")
	newAction.save()
	utilities.actionManager.processActions()
	return newAction


"""
	Get notification object from Action object
"""
def getNotifOfAction(actionObj):
	return actionObj.sourceActionNotification.all()[0]


"""
	Returns True if the given Action object deals with a tool borrow request.
"""
def isToolRequest(actionObj):
	if actionObj.actionType == 'tool':
		return True
	return False


"""
	Returns True if the given Action object deals with a shed request.
"""
def isShedRequest(actionObj):
	if actionObj.actionType == 'shed':
		return True
	return False


"""
	Returns a list of all Action objects in the database.
"""
def getAllActions():
	return Action.objects.all()


"""
	Returns a list of all Action objects requested by a given Profile.
"""
def getProfileAction(profileObj):
	return Action.objects.filter(requester=profileObj)


"""
	Returns a list of all Action objects associated with a given shed.
"""
def getShedActions(shedObj):
	return Action.objects.filter(shed=shedObj)


"""
	Returns a list of all Action objects associated with tool borrowing.
"""
def getToolActions(toolObj):
	return Action.objects.filter(tool=toolObj)

"""
	Returns a single Action object that is related to a tool
	that is currently being borrowed. This is a helper function
	for toolUtilities.returnTool()
"""
def getBorrowedToolAction(toolObj):
	allToolActions = Action.objects.filter(tool=toolObj)
	for action in allToolActions:
		if (action.tool.isAvailable == False):
			return action
	# this is a hacky approach but if we can't find the tool that is
	# being borrowed we'll just return the first one instead of causing
	# problems..screw it..
	return allToolActions[0]


"""
	Gets all notifications tied to action object
"""
def getAllActionNotifications(actionObj):
	return Notification.objects.filter(source = actionObj)

