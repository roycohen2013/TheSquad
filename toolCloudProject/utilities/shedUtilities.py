"""
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
	Create a new shed owned by a given Profile.
"""
def createNewShed(ownerProfileObj,name,location,sharezone,status):
	newShed = Shed(name=name,owner=ownerProfileObj,location=location, \
					sharezone=sharezone,status=status)
	newShed.save()
	return newShed


"""
	Find Shed based on name of shed.
"""
def getShedByName(name):
	return Shed.objects.filter(name=name)


"""
	Adds a tool to a shed.
"""
def addToolToShed(shedObj, toolObj):
	toolObj.myShed = shedObj
	toolObj.save()
	return toolObj


"""
	Remove a tool from a shed. Returns old location
"""
def removeToolFromShed(shedObj, toolObj):
	toolObj.myShed = None
	toolObj.save()
	return shedObj


"""
	Get all sheds in the entire database.
	(regardless of sharezone)
"""
def getAllShedsAllSharezones():
	return Shed.objects.order_by('name')


"""
	Get a shed with its ID
"""
def getShedFromID(id):
	return Shed.objects.get(id=id)

	
"""
	Get all sheds in a given sharezone.
"""
def getAllShedsInSharezone(sharezone):
	return Shed.objects.filter(sharezone=sharezone).order_by('name')


"""
    Get all sheds a user owns
"""
def getAllShedsOwnedBy(profileObj):
	return Shed.objects.filter(owner=profileObj).order_by('name')


"""
    Get all sheds a user is a member of
"""
def getAllShedsJoinedBy(profileObj):
	return profileObj.memberOfShed.order_by('name')


"""
    Check if a user is a member of a shed
"""
def checkForMembership(profileObj, id):
	shed = getShedFromID(id)
	sheds = getAllShedsJoinedBy(profileObj)
	return shed in sheds
	

"""
    Get all sheds a user is an admin of
"""
def getAllShedsAdministratedBy(profileObj):
        return profileObj.adminOfShed

"""
	Get all members of a shed.
"""
def getAllMembersOfShed(shedObj):
	return shedObj.members.order_by('user__username')


"""
	Add a member to a shed. Returns an updated list of all members.
"""
def addMemberToShed(shedObj, profileObj):
	shedObj.members.add(profileObj)
	shedObj.save()
	return shedObj.members.all()


"""
	Remove a member from a shed. Returns an updated list of all members.
"""
def removeMemberFromShed(shedObj, profileObj):
	shedObj.members.remove(profileObj)
	shedObj.save()
	return shedObj.members.all()


"""
	Get all admins of shed.
"""
def getAllAdminsOfShed(shedObj):
	return shedObj.admins.order_by('user__username')


"""
	Add an admin to a shed. Returns an updated list of all admins.
"""
def addAdminToShed(shedObj, profileObj):
	shedObj.admins.add(profileObj)
	shedObj.save()
	return shedObj.admins.all()


"""
	Remove an admin from a shed. Returns an updated list of all admins.
"""
def removeAdminFromShed(shedObj, profileObj):
	shedObj.admins.remove(profileObj)
	shedObj.save()
	return shedObj.admins.all()


"""
	Get name of shed.
"""
def getNameOfShed(shedObj):
	return shedObj.name


"""
	Update name of shed.
"""
def updateNameOfShed(shedObj, newName):
	shedObj.name = newName
	shedObj.save()
	return shedObj


"""
	Get owner of shed.
"""
def getOwnerOfShed(shedObj):
	return shedObj.owner


"""
	Get the location of the shed.
"""
def getLocationOfShed(shedObj):
	return shedObj.location


"""
	Update the location of the shed.
"""
def updateLocationOfShed(shedObj, newLocation):
	shedObj.location = newLocation
	shedObj.save()
	return shedObj


"""
	Get the sharezone of a shed.
"""
def getSharezoneOfShed(shedObj):
	return shedObj.sharezone


"""
	Get the longitude of a shed.
"""
def getLongitudeOfShed(shedObj):
	return shedObj.longitude


"""
	Update the longitude of the shed.
"""
def updateLongitudeOfShed(shedObj, newLongitude):
	shedObj.longitude = newLongitude
	shedObj.save()
	return shedObj.longitude


"""
	Get the latitude of the shed.
"""
def getLatitudeOfShed(shedObj):
	return shedObj.latitude


"""
	Update the latitude of the shed.
"""
def updateLatitudeOfShed(shedObj, newLatitude):
	shedObj.latitude = newLatitude
	shedObj.save()
	return shedObj.latitude
