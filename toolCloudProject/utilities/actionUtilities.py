"""
	Provides functionality for all Action objects.
	(tool borrowing and shed requests)
"""

import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed,Notification,Action

"""
	Creates a new Action object for a Profile requesting to borrow a Tool.
	The currentState field for the object is set to "userBorrowRequest"
"""
def createBorrowRequestAction(tool,requester):
	newAction = Action(tool=tool,requester = requester,actionType="tool",currrentState = "userBorrowRequest")
	newAction.save()
	return newAction


"""
	Creates a new Action object for a Profile requesting to join a Shed.
	The currentState field for the object is set to "userShedRequest"
"""
def createShedRequestAction(shed,requester):
	newAction = Action(shed=shed,requester = requester,actionType="shed",currrentState= "userShedRequest")
	newAction.save()
	return newAction


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
	gets all notifications tied to action object
"""
def getAllActionNotifications(actionObj):
	return Notification.objects.filter(source = actionObj)






