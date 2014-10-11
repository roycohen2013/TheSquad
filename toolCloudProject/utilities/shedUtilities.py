"""
$Date $
$Revision $
$Author $
Provides functionality for all front end requests regarding sheds.
"""

import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed


"""
	Get name of shed.
"""
def getNameOfShed(shedObj):
	return shedObj.name

"""
	Update name of shedObj.
"""
def updateNameOfShed(shedObj, newName):
	shedObj.name = newName
	shedObj.save()
	return shedObj

"""
	Get owner of shedObj.
"""
def getOwnerOfShed(shedObj):
	return shedObj.ownerID


"""
	Get admins of shedObj.
"""
def getAdminsOfShed(shedObj):
	return shedObj.admins


"""
	Add an admin to a shedObj.
"""
def addAdminToShed(shedObj, profile):
	oldAdmins = shedObj.admins
	newAdmins = oldAdmins + str(profile.pk)
	shedObj.admins = newAdmins
	shedObj.save()
	return shedObj


"""
	Remove an admin from a shedObj.
"""
def removeAdminFromShed(shedObj, profile):
	adminList = shedObj.admins.split(',')
	if profile.pk in adminList:
		adminList.remove(profile.pk)	
		newAdmins = ','.join(adminList)
		shedObj.admins = newAdmins
		shedObj.save()
	return shedObj.admins

"""
	Get the members of a shedObj.
"""
def getMembersOfShed(shedObj):
	return shedObj.members


"""
	Add a member to a shedObj.
"""
def addMemberToShed(shedObj, profile):
	shedObj.members = shedObj.members + ',' + str(profile.pk)
	return shedObj.members


"""
	Remove a member from the shedObj.
"""
def removeMemberFromShed(shedObj, profile):
	memberList = shedObj.members.split(',')
	if profile.pk in adminList:
		memberList.remove(profile.pk)	
		newMembers = ','.join(memberList)
		shedObj.members = newMembers
		shedObj.save()
	return shedObj.members


"""
	Get the location of the shedObj.
"""
def getLocationOfShed(shedObj):
	return shedObj.location


"""
	Update the location of the shedObj.
"""
def updateLocationOfShed(shedObj, newLocation):
	shedObj.location = newLocation
	shedObj.save()
	return shedObj


"""
	Get the sharezone of a shedObj.
"""
def getSharezoneOfShed(shedObj):
	return shedObj.sharezone


"""
	Get the longitude of a shedObj.
"""
def getLongitudeOfShed(shedObj):
	return shedObj.longitude


"""
	Update the longitude of the shedObj.
"""
def updateLongitudeOfShed(shedObj, newLongitude):
	shedObj.longitude = newLongitude
	shedObj.save()
	return shedObj.longitude


"""
	Get the latitude of the shedObj.
"""
def getLatitudeOfShed(shedObj):
	return shedObj.latitude


"""
	Update the latitude of the shedObj.
"""
def updateLatitudeOfShed(shedObj, newLatitude):
	shedObj.latitude = newLatitude
	shedObj.save()
	return shedObj.latitude
