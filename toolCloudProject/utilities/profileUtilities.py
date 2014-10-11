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
	Return a list of all profiles in the database
"""
def listAllProfiles():
	return Profile.objects.all()


"""
	Get the Django User object related to this Profile.
"""
def getUserofProfile(profileID):
	return profile.user


"""
	Get the Profile object related to this User object.
"""
def getProfileFromUser(userID):
	return Profile.objects.get(user=userID)

"""
	Get the phone number of a Profile.
"""
def getPhoneNumber(profile):
	return profile.phoneNumber

"""
	Update the phone number of a Profile.
"""
def updatePhoneNumber(profile, newNumber):
	profile.phoneNumber = newNumber
	profile.save()
	return profile


"""
	Get the address of a Profile.
"""
def getAddress(profile):
	return profile.address


"""
	Update the address of a profile.
"""
def updateAddress(profile, newAddress):
	profile.address = newAddress
	profile.save()
	return profile


"""
	Get the reputation of a Profile.
"""
def getReputation(profile):
	return profile.reputation


"""
	Update the reputation of a profile by a factor. The new reputation will be
	the old reputation multiplied by the factor.
"""
def updateReputation(profile, factor):
	profile.reputation = (profile.reputation * factor)
	profile.save()
	return profile


"""
	Get the sharezone of a Profile.
"""
def getSharezone(profile):
	return profile.sharezone


"""
	Update the sharezone of a Profile.
"""
def updateSharezone(profile, newSharezone):
	profile.sharezone = newSharezone
	profile.save()
	return profile
