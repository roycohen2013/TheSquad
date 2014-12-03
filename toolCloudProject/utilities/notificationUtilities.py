"""
    Provides functionality for all front end requests regarding notifications.
"""

import utilities.actionManager as actionManager
import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from toolCloudApp.models import Profile, Tool, Shed, Notification, Action
from mailSend import sendMail

"""
    Create a new object of the "info" type with no recipientProfile or source

    Only used for non-saved 'throw-away' notifications like failed login
"""
def createTempInfoNotif(content, typ):
    class Object(object):
        pass
    a = Object()
    a.content = content
    a.notificationType = typ
    return a

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

    #send confirmation email
    sendMail(recipientProfile, "You have a new notification!", + content)
    #actionManager.processActions()
    return newNotification

def createBadInfoNotif(sourceObj,recipientProfile,content):
    if isinstance(sourceObj, Shed):
        newNotification = Notification(sourceShed = sourceObj, content = content, recipient = recipientProfile, notificationType = "alert")
    elif isinstance(sourceObj, Tool):
        newNotification = Notification(sourceTool = sourceObj, content = content, recipient = recipientProfile, notificationType = "alert")
    elif isinstance(sourceObj, Profile):
       newNotification = Notification(sourceProfile = sourceObj, content = content, recipient = recipientProfile, notificationType = "alert")
    elif isinstance(sourceObj, Action):
        newNotification = Notification(sourceAction = sourceObj, content = content, recipient = recipientProfile, notificationType = "alert")

    newNotification.save()
    sendMail(recipientProfile, "You have a new notification!", + content)
    #actionManager.processActions()
    return newNotification
"""
    Create a new Notification that waits for a response.
"""
def createResponseNotif(sourceObj,recipientProfile,content,options):
    if isinstance(sourceObj, Shed):
        newNotification = Notification(sourceShed = sourceObj, options=options, content = content, recipient = recipientProfile, notificationType = "request")
    elif isinstance(sourceObj, Tool):
        newNotification = Notification(sourceTool = sourceObj, options=options, content = content, recipient = recipientProfile, notificationType = "request")
    elif isinstance(sourceObj, Profile):
       newNotification = Notification(sourceProfile = sourceObj, options=options, content = content, recipient = recipientProfile, notificationType = "request")
    elif isinstance(sourceObj, Action):
        newNotification = Notification(sourceAction = sourceObj, options=options, content = content, recipient = recipientProfile, notificationType = "request")

    newNotification.save()
    sendMail(recipientProfile, "You have a new notification!", + content)
    #actionManager.processActions()
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
    For tool borrow request notification when the recipient clicks
    "Accept" button. This will change the response of the notification
    to "Accept" which will be handled by actionManager.py and will delete
    the notification from the database.
"""
def acceptBorrowRequest(notifObj):
    notifObj.response = "Accept"
    notifObj.save()
    actionManager.processActions()

"""
    For tool borrow request notification when the recipient clicks
    "Deny" button. This will change the response of the notification
    to "Deny" which will be handled by actionManager.py and will delete
    the notification from the database and send a notification to the
    requester of the tool saying you've been declined.
"""
def denyBorrowRequest(notifObj):
    notifObj.response =  "Deny"
    notifObj.save()
    actionManager.processActions()

def confirmReturn(notifObj):
    notifObj.response = "Yes"
    notifObj.save()
    actionManager.processActions()

def denyReturn(notifObj):
    notifObj.response = "No"
    notifObj.save()
    actionManager.processActions()

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
    return notifObj.sourceAction

        
"""
    Returns the type of the notification source in string format.
        Source of type Tool returns "Tool"
        Source of type Shed returns "Shed"
        Source of type Profile returns "Profile"
        Source of type Action returns "Action"
        If source is not one of those, return ""
"""
def getNotifSourceType(notifObj):
    if notifObj.sourceShed != None:
        return 'Shed'
    elif notifObj.sourceTool != None:
        return 'Tool'
    elif notifObj.sourceProfile != None:
        return 'Profile'
    elif notifObj.sourceAction != None:
        return 'Action'


"""
    Returns True if notification source is a Shed object.
"""
def isNotifFromShed(notifObj):
    if notifObj.sourceShed != None:
        return True
    return False


"""
    Returns True if notification source is a Tool object.
"""
def isNotifFromTool(notifObj):
    if notifObj.sourceTool != None:
        return True
    return False


"""
    Returns True if notification source is a Profile object.
"""
def isNotifFromProfile(notifObj):
    if notifObj.sourceProfile != None:
        return True
    return False


"""
    Returns True if notification source is a Action object.
"""
def isNotifFromAction(notifObj):
    if notifObj.sourceAction != None:
        return True
    return False


"""
    Returns True if the notification has been responded to.
"""
def notifHasResponse(notifObj):
    return (notifObj.response is not None)
    #if (notifObj.response == ""):
    #    return False
    #return True


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
    return notifObj


"""
    Deletes a notification that is no longer needed.
"""
def deleteNotif(notifObj):
    notifObj.delete()

