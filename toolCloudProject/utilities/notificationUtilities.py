"""
    Provides functionality for all front end requests regarding notifications.
"""

import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from toolCloudApp.models import Profile, Tool, Shed, Notification

"""
    Create a new Notification of the "info" type.
"""
<<<<<<< HEAD
def createInfoNotif(sourceObj,recipientProfile,content):
=======
def createNotificationInfo(sourceObj,recipientProfile,content):
>>>>>>> FETCH_HEAD
	newNotification = Notification(source = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
	newNotification.save()
	return newNotification

<<<<<<< HEAD

"""
    Create a new Notification that waits for a response.
"""
def createResponseNotif(sourceObj,recipientProfile,content):
    newNotification = Notification(source=sourceObj, content = content, recipient=recipientProfile,notificationType="request")
    newNotification.save()
    return newNotification


=======
>>>>>>> FETCH_HEAD
"""
    Get the source of a notification.
"""
def getNotifSource(notifObj):
    return notifObj.source

"""
    Get the recipient of a notification.
"""
def getNotifRecip(notifObj):
    return notifObj.recipient

"""
    Get the content of a notification.
"""
def getNotifContent(notifObj):
    return notifObj.content


"""
    Returns True if an "info" notification.
"""
def isInfoNotif(notifObj):
    if notifObj.notificationType == 'info':
        return True
    return False

"""
    Returns True if a "request" notification.
"""
def isRequestNotif(notifObj):
    if notifObj.notificationType == 'request':
        return True
    return False

"""
    Deletes a notification that is no longer needed.
"""
def deleteNotif(notifObj):
    notifObj.delete()

"""
    Gets all the notifications for a Profile object.
"""
def getAllProfileNotifs(profileObj):
    return Notification.objects.filter(recipient=profileObj)

"""
    Returns True if notification source is a Shed object.
"""
def isNotifFromShed(notifObj):
    if isinstance(notifObj.source, Shed):
        return True
    return False

"""
    Returns True if notification source is a Tool object.
"""
def isNotifFromTool(notifObj):
    if isinstance(notifObj.source, Tool):
        return True
    return False

"""
    Returns True if notification source is a Profile object.
"""
def isNotifFromProfile(notifObj):
    if isinstance(notifObj.source, Profile):
        return True
    return False

"""
    Returns True if notification source is a Action object.
"""
def isNotifFromAction(notifObj):
    if isinstance(notifObj.source, Action):
        return True
    return False

    
