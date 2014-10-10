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
def getNameOfShed(shed):
	return shed.name

"""
	Update name of shed.
"""
def updateNameOfShed(shed, newName):
	shed.name = newName
	shed.save()
	return shed

"""
	Get owner of shed.
"""
def getOwnerOfShed(shed):
	return shed.ownerID


"""
	Get admins of shed.
"""
def getAdminsOfShed(shed):
	return shed.admins


"""
	Add an admin to a shed.
"""
def addAdminToShed(shed, profile):
	oldAdmins = shed.admins
	newAdmins = oldAdmins + str(profile.pk)
	shed.admins = newAdmins
	shed.save()
	return shed


"""
	Remove an admin from a shed.
"""
def removeAdminFromShed(shed, profile):
	adminList = shed.admins.split(',')
	if profile.pk in adminList:
		adminList.remove(profile.pk)	
		newAdmins = ','.join(adminList)
		shed.admins = newAdmins
		shed.save()
	return shed.admins

"""
	Get the members of a shed.
"""
def getMembersOfShed(shed):
	return shed.members


"""
	Add a member to a shed.
"""
def addMemberToShed(shed, profile):
	shed.members = shed.members + ',' + str(profile.pk)
	return shed.members


"""
	Remove a member from the shed.
"""
def removeMemberFromShed(shed, profile):
	memberList = shed.members.split(',')
	if profile.pk in adminList:
		memberList.remove(profile.pk)	
		newMembers = ','.join(memberList)
		shed.members = newMembers
		shed.save()
	return shed.members


"""
	Get the location of the shed.
"""
def getLocationOfShed(shed):
	return shed.location


"""
	Update the location of the shed.
"""
def updateLocationOfShed(shed, newLocation):
	shed.location = newLocation
	shed.save()
	return shed


"""
	Get the sharezone of a shed.
"""
def getSharezoneOfShed(shed):
	return shed.sharezone


"""
	Get the longitude of a shed.
"""
def getLongitudeOfShed(shed):
	return shed.longitude


"""
	Update the longitude of the shed.
"""
def updateLongitudeOfShed(shed, newLongitude):
	shed.longitude = newLongitude
	shed.save()
	return shed.longitude


"""
	Get the latitude of the shed.
"""
def getLatitudeOfShed(shed):
	return shed.latitude


"""
	Update the latitude of the shed.
"""
def updateLatitudeOfShed(shed, newLatitude):
	shed.latitude = newLatitude
	shed.save()
	return shed.latitude
