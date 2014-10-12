"""
	Our database tables.
"""


from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User)
	timeCreated = models.DateTimeField(auto_now_add=True)
	phoneNumber = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	sharezone = models.CharField(max_length=5) #five digit zip code
	status = models.CharField(max_length=50)
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	reputation = models.IntegerField(default=50) #0..100 rating
	preferences = models.CharField(max_length=50)

	#registered = models.IntegerField(default=0) #0: user has not yet completed their profile, 1: user can login and use
	# all features of site

	def __str__(self):
		myList = ["Name: " + self.user.first_name + " " + self.user.last_name, \
					"Sharezone: " + self.sharezone]
		return " ".join(myList)


class Shed(models.Model):
	timeCreated = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)
	owner = models.OneToOneField('Profile') #the Profile who owns this shed
	admins = models.ManyToManyField('Profile',related_name='adminOfShed',null=True) #admins of shed
	members = models.ManyToManyField('Profile',related_name='memberOfShed',null=True) #members of shed
	location = models.CharField(max_length=75) #address of the shed
	sharezone = models.CharField(max_length=5) #five digit zip code
	latitude = models.IntegerField(default=-1)
	longitude = models.IntegerField(default=-1)
	status = models.CharField(max_length=50)
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	preferences = models.CharField(max_length=50)

	def __str__(self):
		myList = ["Name: " + self.name, "Sharezone: " + self.sharezone, \
						"Owned by " + self.ownerID.user.username]
		return ",".join(myList)

class Tool(models.Model):
	timeCreated = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	tags = models.CharField(max_length=200) #categories that apply to this tool object
	owner = models.OneToOneField('Profile', related_name='owner_ID') #the Profile who owns this tool
	borrower = models.OneToOneField('Profile',null=True, related_name='borrower_ID') # the Profile who is borrowing the tool
	myShed = models.OneToOneField('Shed',null=True) #the Shed this tool is apart of
	location = models.CharField(max_length=75) #current location of the tool
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	condition = models.IntegerField(default=0) #0-10 scale
	isAvailable = models.IntegerField() # 0 if not available, 1 if available
	borrowedCount = models.IntegerField(default=0) # times Tool borrowed
	requestedCount = models.IntegerField(default=0) # times Tool requested
	preferences = models.CharField(max_length=50) #serialized JSON object

	def __str__(self):
		myList = ["Name: " + self.name, "Owned by " + self.ownerID.user.username, \
					"Borrowed by" + self.borrowerID, "My shed: " + self.myShed.name]
		return ",".join(myList)


class Notification(models.Model):
	content = models.CharField(max_length=50) #serialized JSON object


class Action(models.Model):
	content = models.CharField(max_length=50) #serialized JSON object
