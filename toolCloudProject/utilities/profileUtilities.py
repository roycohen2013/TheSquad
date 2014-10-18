"""
$Date $
$Revision $
$Author $

Provides functionality for all front end requests regarding profiles.
"""

import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed


"""
	Create a new Profile and save it to the database.
"""
def createNewProfile(firstName,lastName,username,email,password,phoneNumber, \
										address,sharezone,status,preferences):
	newProfile = Profile(user = User.objects.create_user(username,email,password), \
						phoneNumber = phoneNumber, address = address, sharezone = sharezone, \
						status = status, preferences = preferences)
	newProfile.user.first_name = firstName
	newProfile.user.last_name = lastName
	newProfile.user.save()
	newProfile.save()
	return newProfile


"""
	Return a list of all profile objects in the entire database.
	(regardless of sharezone)
"""
def getAllProfiles():
	return Profile.objects.all()


"""
	Return a list of all profiles in a specific sharezone.
"""
def getAllProfilesInSharezone(sharezone):
	return Profile.objects.filter(sharezone=sharezone)

def getAllOtherProfilesInSharezone(profileObj):
	sharezone = profileObj.sharezone
	return Profile.objects.filter(sharezone=sharezone).exclude(user__username = profileObj.user.username)

"""
	Get the Django User object related to this Profile object.
"""
def getUserofProfile(profileObj):
	return profileObj.user


"""
	Get the Profile object related to this User object.
"""
def getProfileFromUser(userObj):
	return userObj.myProfile


"""
	Get the first name of a Profile object.
"""
def getFirstName(profileObj):
	return profileObj.user.first_name


"""
	Update the first name of a Profile object.
"""
def updateFirstName(profileObj, newFirstName):
	profileObj.user.first_name = newFirstName
	profileObj.user.save()
	profileObj.save()
	return profileObj


"""
	Get the last name of a Profile object.
"""
def getLastName(profileObj):
	return profileObj.user.last_name


"""
	Update the last name of a Profile object.
"""
def updateLastName(profileObj, newLastName):
	profileObj.user.last_name = newLastName
	profileObj.user.save()
	profileObj.save()
	return profileObj


"""
	Get the username of a Profile object.
"""
def getUsername(profileObj):
	return profileObj.user.username


"""
	Get email of a Profile object.
"""
def getEmail(profileObject):
	return profileObj.user.email


"""
	Get the phone number of a Profile object.
"""
def getPhoneNumber(profileObj):
	return profileObj.phoneNumber


"""
	Update the phone number of a Profile object.
"""
def updatePhoneNumber(profileObj, newNumber):
	profileObj.phoneNumber = newNumber
	profileObj.save()
	return profileObj


"""
	Get the address of a Profile object.
"""
def getAddress(profileObj):
	return profileObj.address


"""
	Update the address of a Profile object.
"""
def updateAddress(profileObj, newAddress):
	profileObj.address = newAddress
	profileObj.save()
	return profileObj


"""
	Get the reputation of a Profile object.
"""
def getReputation(profileObj):
	return profileObj.reputation


"""
	Update the reputation of a Profile by a factor. The new reputation will be
	the old reputation multiplied by the factor.
"""
def updateReputation(profileObj, factor):
	profileObj.reputation = (profileObj.reputation * factor)
	profileObj.save()
	return profileObj


"""
	Get the sharezone of a Profile object.
"""
def getSharezone(profileObj):
	return profileObj.sharezone


"""
	Update the sharezone of a Profile object.
"""
def updateSharezone(profileObj, newSharezone):
	profileObj.sharezone = newSharezone
	profileObj.save()
	return profileObj


"""
	Get the status of a Profile object.
"""
def getStatus(profileObj):
	return profileObj.status


"""
	Update the status of a Profile object.
"""
def updateStatus(profileObj, newStatus):
	profileObj.status = newStatus
	profileObj.save()
	return profileObj
