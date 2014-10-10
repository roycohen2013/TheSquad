"""
$Date $
$Revision $
$Author $
"""

from django.contrib.auth.models import User
from toolCloudApp.models import Profile
from django.utils import timezone

"""This script will create a new user object (in django's default models)
AND a new profile object (from Squad models)

called during new user registration

written by Jackson and Roy
"""

def newUser(firstname, lastname, username, email, password):
	userObject = User.objects.create_user(username, email, password)
	userObject.last_name = lastname
	userObject.first_name = firstname
	return userObject

def newProfile(userObject, phonenumber, address):
	profileObject = Profile(user=userObject)
	profileObject = timezone.now()
	profileObject.phoneNumber = phonenumber
	"""start of possibly bad code - may need fixing depending on 
	how frontend handles address and sends here (as of now assumes the
		address is a string)
	"""
	profileObject.address = address
	profileObject.shareZone	= address[-5:]	#slice end off of address string
	"""end of possibly bad code
	"""
	profileObject.reputation = 50	#set reputation to 50 (default value)
	"""default preference object should be assigned
	"""
	profileObject.preferences = ''
	"""end of possibly bad code
	"""
	return profileObject

UserObject = newUser(firstname, lastname, username, email, password)
UserObject.save()

ProfileObject = newProfile(UserObject, phonenumber, address)
ProfileObject.save()

return profileObject