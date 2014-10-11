from django.db import models
from django.contrib.auth.models import User

"""
Django automatically gives every object of our classes a unique primary key.
Each time you create an object (insert a row into the table), that object
will have a primary key associated with it that is different from all other
objects in that specific class. Primary keys start from 1 and increase by 1
for every object created.

How this model works (or so we hope):

Get the owner of a Shed: get the Shed object's ownerID
Get all Sheds that a Profile owns: filter thru all Sheds looking for ownerID
Get all the admins of a Shed: get the Shed object's admins
Get all Tools in a Shed: filter thru list of all Tool objects that have a specific myShed
Get all available Tools in a Shed: same as above but also look for Tools that have isAvailable == 1
Get the current borrower of a Tool: get the borrowerID from the Tool object
Get all Profiles that have access to a Shed: get the Shed object's members
Get all Profiles apart of a sharezone: filter thru all Profile objects that have a specific sharezone
Get all Sheds apart of a sharezone: filter thru all the Shed objects that have a specific sharezone
"""

class Profile(models.Model):
	user = models.OneToOneField(User)
	timeCreated = models.DateTimeField(auto_now_add=True)
	#firstName = models.CharField(max_length=50) part of django's user class
	#lastName = models.CharField(max_length=50)	 part of django's user class
	phoneNumber = models.CharField(max_length=50)
	#email = models.EmailField()				 part of django's user class
	address = models.CharField(max_length=100)
	sharezone = models.CharField(max_length=5) #five digit zip code
	status = models.CharField(max_length=50)
	picture = models.CharField(max_length=50) #path to image file
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	reputation = models.IntegerField(default=50) #0..100 rating
	preferences = models.CharField(max_length=50) #serialized JSON object

	#registered = models.IntegerField(default=0) #0: user has not yet completed their profile, 1: user can login and use
	# all features of site

	def __str__(self):
		myList = [self.sharezone, self.timeCreated]
		return ",".join(myList)

class Shed(models.Model):
	timeCreated = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)
	ownerID = models.OneToOneField('Profile') #the Profile who owns this shed
	admins = models.CharField(max_length=100) #CSV containing primary keys of Profiles who are admins
	members = models.CharField(max_length=200) #CSV containing primary keys of Profiles with access to Shed
	location = models.CharField(max_length=75) #address of the shed
	sharezone = models.CharField(max_length=5) #five digit zip code
	latitude = models.IntegerField(default=-1)
	longitude = models.IntegerField(default=-1)
	status = models.CharField(max_length=50)
	picture = models.CharField(max_length=50) #path to image file
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	preferences = models.CharField(max_length=50) #serialized JSON object

	def __str__(self):
		myList = [self.name, self.sharezone, self.ownerID, self.admins, self.members]
		return ",".join(myList)

class Tool(models.Model):
	timeCreated = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	tags = models.CharField(max_length=200) #categories that apply to this tool object
	ownerID = models.OneToOneField('Profile', null=True, related_name='owner_ID') #the Profile who owns this tool
	borrowerID = models.OneToOneField('Profile',null=True, related_name='borrower_ID') # the Profile who is borrowing the tool
	myShed = models.OneToOneField('Shed',null=True) #the Shed this tool is apart of
	location = models.CharField(max_length=75) #current location of the tool
	picture = models.CharField(max_length=50) #path to image file
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	condition = models.IntegerField(default=0) #0-10 scale
	isAvailable = models.IntegerField() # 0 if not available, 1 if available
	borrowedCount = models.IntegerField(default=0) # times Tool borrowed
	requestedCount = models.IntegerField(default=0) # times Tool requested
	preferences = models.CharField(max_length=50) #serialized JSON object

	def __str__(self):
		myList = [self.name, self.ownerID, self.borrowerID, self.myShed, \
					self.condition, self.isAvailable, self.timeCreated]
		return ",".join(myList)

class Notification(models.Model):
	content = models.CharField(max_length=50) #serialized JSON object

class Action(models.Model):
	content = models.CharField(max_length=50) #serialized JSON object
