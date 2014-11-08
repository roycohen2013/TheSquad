from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from toolCloudApp.models import Profile, Tool, Shed, Notification





def createNotificationInfo(sourceObj,recipientProfile,content):
	newNotification = Notification(source = sourceObj, content = content, recipient = recipientProfile, notificationType = "info")
	newNotification.save()
	return newNotification



