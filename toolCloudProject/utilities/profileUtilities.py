"""
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
										address,sharezone,city,state,status,preferences_privacy):
	newProfile = Profile(user = User.objects.create_user(username,email,password), \
						phoneNumber = phoneNumber, streetAddress = address, sharezone = sharezone, \
						city = city, state = state, \
						status = status, preferences_Privacy = preferences_privacy)
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
	return Profile.objects.order_by('user__first_name')


"""
	Return a list of all profiles in a specific sharezone.
"""
def getAllProfilesInSharezone(sharezone):
	return Profile.objects.filter(sharezone=sharezone).order_by('user__username')


"""
	Returns a list of all profiles in a specific sharezone other than me.
"""
def getAllOtherProfilesInSharezone(profileObj):
	sharezone = profileObj.sharezone
	return Profile.objects.filter(sharezone=sharezone).exclude(user__username = profileObj.user.username).order_by('user__username')


"""
	Get the Django User object related to this Profile object.
"""
def getUserOfProfile(profileObj):
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
def getEmail(profileObj):
	return profileObj.user.email


"""
	Update email of a profile object.
"""
def updateEmail (profileObj, email):
	profileObj.user.email = email
	profileObj.user.save()
	profileObj.save()
	return profileObj

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
	Get the street address of a Profile object.
"""
def getAddress(profileObj):
	return profileObj.streetAddress


"""
	Get the city of a Profile object
"""
def getCity(profileObj):
	return profileObj.city


"""
	Get the state of a Profile object
"""
def getState(profileObj):
	return profileObj.state


def getStateName(profileObj):
	return profileObj.stateName
	

"""
	Update the entire address of a Profile object(street, city, state, sharezone)
"""
def updateAddress(profileObj, newStreetAddress, newCity, newState, newSharezone):
	profileObj = updateStreetAddress(profileObj, newStreetAddress)
	profileObj = updateCity(profileObj, newCity)
	profileObj = updateState(profileObj, newState)
	profileObj = updateSharezone(profileObj, newSharezone)
	profileObj.save()
	return profileObj


"""
	Update the  street address of a Profile object.
"""
def updateStreetAddress(profileObj, newAddress):
	profileObj.streetAddress = newAddress
	profileObj.save()
	return profileObj


"""
	Update the city of a Profile object
"""
def updateCity(profileObj, newCity):
	profileObj.city = newCity
	profileObj.save()
	return profileObj


"""
	Update the state of a Profile object
"""
def updateState(profileObj, newState):
	profileObj.state = newState
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


"""
	Get Profile pbject for username
"""
def getProfileFromUsername (user_name):
	embeddeduser = User.objects.get (username = user_name)
	return Profile.objects.get (user = embeddeduser)

