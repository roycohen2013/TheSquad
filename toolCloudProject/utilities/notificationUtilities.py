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
from toolCloudApp.models import Profile, Tool, Shed, Notification, Action


"""
    Create a new Notification of the "info" type.
"""





def createInfoNotif(sourceObj,recipientProfile,content):
    if isinstance(sourceObj, Shed):
        newNotification = Notification(sourceShed = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
    elif isinstance(sourceObj, Tool):
        newNotification = Notification(sourceTool = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
    elif isinstance(sourceObj, Profile):
       newNotification = Notification(sourceProfile = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
    elif isinstance(sourceObj, Action):
        newNotification = Notification(sourceAction = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")


    newNotification.save()
    return newNotification


"""
    Create a new Notification that waits for a response.
"""
def createResponseNotif(sourceObj,recipientProfile,content):
    if isinstance(sourceObj, Shed):
        newNotification = Notification(sourceShed = sourceObj, content = content, recipient = recipientProfile, notificationType = "request")
    elif isinstance(sourceObj, Tool):
        newNotification = Notification(sourceTool = sourceObj, content = content, recipient = recipientProfile, notificationType = "request")
    elif isinstance(sourceObj, Profile):
       newNotification = Notification(sourceProfile = sourceObj, content = content, recipient = recipientProfile, notificationType = "request")
    elif isinstance(sourceObj, Action):
        newNotification = Notification(sourceAction = sourceObj, content = content, recipient = recipientProfile, notificationType = "request")

    # newNotification = Notification(source=sourceObj, content = content, recipient=recipientProfile,notificationType="request")
    newNotification.save()
    return newNotification


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
    Gets all the notifications for a Profile object.
"""
def getAllProfileNotifs(profileObj):
    return Notification.objects.filter(recipient=profileObj)


"""
    Gets all the not yet responded to notifications of a Profile object.
    This includes info notifs as well as request notifs that have null
    response fields.
"""
def getAllActiveProfileNotifs(profileObj):
    return Notification.objects.filter(recipient=profileObj, response=None)


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
    Get the source object of a notification.
"""
def getNotifSourceObject(notifObj):
    if isinstance(notifObj.source, Shed):
       return sourceShed
    elif isinstance(notifObj.source, Tool):
        return sourceTool
    elif isinstance(notifObj.source, Profile):
        return sourceProfile
    elif isinstance(notifObj.source, Action):
        return sourceAction



"""
    Returns the type of the notification source in string format.
        Source of type Tool returns "Tool"
        Source of type Shed returns "Shed"
        Source of type Profile returns "Profile"
        Source of type Action returns "Action"
        If source is not one of those, return ""
"""
def getNotifSourceType(notifObj):
    if isinstance(notifObj.source, Shed):
        return 'Shed'
    elif isinstance(notifObj.source, Tool):
        return 'Tool'
    elif isinstance(notifObj.source, Profile):
        return 'Profile'
    elif isinstance(notifObj.source, Action):
        return 'Action'
    else:
        return ''


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
    notifObj.save()


"""
    Deletes a notification that is no longer needed.
"""
def deleteNotif(notifObj):
    notifObj.delete()

