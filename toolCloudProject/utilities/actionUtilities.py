"""
	Provides functionality for all interactions with Actions
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
	tool = models.ForeignKey('Tool', related_name='toolActions')#if tool, send to owner of tool
	shed = models.ForeignKey('Shed', related_name='shedActions')#if shed, send to all admins of shed
	admin = models.ForeignKey('Profile', related_name='adminActions')#returns list of actions that a user is controlling of
	requester = models.ForeignKey('Profile', related_name='requesterActions')

	actionType = models.CharField(max_length=20)#either tool, or shed
	currrentState = models.CharField(max_length=20)
	timestamps = models.CharField(max_length=560)#CSV timestamps for every state
	workSpace = models.CharField(max_length=200)#for use in state machine
"""


	#newNotification = Notification(source = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
	#newNotification.save()
	#return newNotification


def createBorrowAction(tool,requester):
	"""
	"""
	newAction = Action(tool=tool,requester = requester,actionType="tool",currrentState = "userBorrowRequest")
	newAction.save()
	return newAction


def createShedRequestAction(shed,requester):
	"""
	"""
	newAction = Action(shed=shed,requester = requester,actionType="shed",currrentState= "userShedRequest")
	newAction.save()
	return newAction



def getAllActions():
	"""
	"""
	return Action.objects.all()

def getBorrowActions():
	pass

def getShedRequestActions():
	pass


def getActionsFromShed():
	pass

def getActionFromTool():
	pass


def isToolRequest():
	pass

def isShedRequest():
	pass

