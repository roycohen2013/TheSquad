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
	Return a list of all profiles in all sharezones.
"""
def listAllProfiles():
	return Profile.objects.all()


"""
	Return a list of all profiles in a sharezone.
"""
def listAllProfilesInSharezone(sharezone):
	return Profile.objects.filter(sharezone=sharezone)


"""
	Get the Django User object related to this Profile.
"""
def getUserofProfile(profileObj):
	return profileObj.user


"""
	Get the Profile object related to this User object.
"""
def getProfileFromUser(userObj):
	return Profile.objects.get(user=userObj)


"""
	Get the first name of a Profile.
"""
def getFirstName(profileObj):
	return profileObj.user.first_name


"""
	Get the last name of a Profile.
"""
def getLastName(profileObj):
	return profileObj.user.last_name


"""
	Get the phone number of a Profile.
"""
def getPhoneNumber(profileObj):
	return profileObj.phoneNumber


"""
	Update the phone number of a Profile.
"""
def updatePhoneNumber(profileObj, newNumber):
	profileObj.phoneNumber = newNumber
	profileObj.save()
	return profileObj


"""
	Get the address of a Profile.
"""
def getAddress(profileObj):
	return profileObj.address


"""
	Update the address of a profile.
"""
def updateAddress(profileObj, newAddress):
	profileObj.address = newAddress
	profileObj.save()
	return profileObj


"""
	Get the reputation of a Profile.
"""
def getReputation(profileObj):
	return profileObj.reputation


"""
	Update the reputation of a profile by a factor. The new reputation will be
	the old reputation multiplied by the factor.
"""
def updateReputation(profileObj, factor):
	profileObj.reputation = (profileObj.reputation * factor)
	profileObj.save()
	return profileObj


"""
	Get the sharezone of a Profile.
"""
def getSharezone(profileObj):
	return profileObj.sharezone


"""
	Update the sharezone of a Profile.
"""
def updateSharezone(profileObj, newSharezone):
	profileObj.sharezone = newSharezone
	profileObj.save()
	return profileObj


"""
	Get the status of a Profile.
"""
def getStatus(profileObj):
	return profileObj.status


"""
	Update the status of a Profile.
"""
def updateStatus(profileObj,status):
	profileObj.status = status
	profileObj.save()
	return profileObj

