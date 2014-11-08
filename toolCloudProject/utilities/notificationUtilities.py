"""
    Provides functionality for all front end requests regarding notifications.
"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from toolCloudApp.models import Profile, Tool, Shed, Notification


"""
    Create a new Notification that requires no response.
"""
def createInfoNotification(sourceObj,recipientProfile,content):
	newNotification = Notification(source = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
	newNotification.save()
	return newNotification


"""
    Create a new Notification that waits for a response.
"""
def createResponseNotification(sourceObj,recipientProfile,content):
    newNotification = Notification(source=sourceObj, content = content, recipient=recipientProfile,notificationType="request")
    newNotification.save()
    return newNotification


"""
    Get the source of a notification.
"""
def getNotificationSource(notifObj):
    return notifObj.source


"""
    Get the recipient of a notification.
"""
def getNotificationRecip(notifObj):
    return notifObj.recipient


"""
    Returns True if an "info" notification.
"""
def isInfoNotification(notifObj):
    if notifObj.notificationType == 'info':
        return True
    return False


"""
    Returns True if a "request" notification.
"""
def isRequestNotification(notifObj):
    if notifObj.notificationType == 'request':
        return True
    return False


"""
    Deletes a notification that is no longer needed.
"""
def deleteNotification(notifObj):
    notifObj.delete()


"""
    Gets all the notifications of a Profile object.
"""
def getAllProfileNotifs(profileObj):
    return Notification.objects.filter(recipient=profileObj)


"""
    Gets all the not yet responded to notifications of a Profile object.
    This includeds info notifs as well as request notifs that have null
    response fields.
"""
def getAllActiveProfileNotifs(profileObj):
    return Notification.objects.filter(recipient=profileObj, response="")


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


"""
    Returns True if the notification has been responded to.
"""
def notifHasResponse(notifObj):
    if (notifObj.response == ""):
        return False
    return True


"""
    Returns the response of a notification. Will return None
    if the notification has not been responded to yet.
"""
def getNotifResponse(notifObj):
    if (notifObj.response != ""):
        return notifObj.response
    return None


"""
    Respond to a notification with text of your choice.
"""
def respondToNotif(notifObj, myResponse):
    notifObj.response = myResponse
