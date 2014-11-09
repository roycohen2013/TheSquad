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


#what calls action manager:
	#Automated
	#update to one of the action objects
	#call back from a notification object


"""
class Action(models.Model):
    tool = models.ForeignKey('Tool', related_name='toolActions',null = True)#if tool, send to owner of tool
    shed = models.ForeignKey('Shed', related_name='shedActions',null = True)#if shed, send to all admins of shed
    requester = models.ForeignKey('Profile', related_name='requesterActions')

    actionType = models.CharField(max_length=20)#either tool, or shed
    currrentState = models.CharField(max_length=20)
    timeStamps = models.CharField(max_length=560,null = True)#CSV timestamps for every state
    workSpace = models.CharField(max_length=200,null = True)#for use in state machine

    content_type = models.ForeignKey(ContentType,null=True,blank=True)
    object_id = models.PositiveIntegerField(null=True,default=1)
"""

	#newNotification = Notification(source = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
	#newNotification.save()
	#return newNotification

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
def getAllActionsRequestedBy(profileObj):
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
	Add a timestamp to this Action object.
"""
def addTimestampToAction(actionObj, timestamp):
	actionObj.timestamp += (timestamp + ',')
	actionObj.save()
	return actionObj

