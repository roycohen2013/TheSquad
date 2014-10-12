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

	preferences_Privacy = models.IntegerField(default=0)
	#publi   0 - you can see everything 
	#private 1 - persons name
	#secret  2 - initials


	#registered = models.IntegerField(default=0) #0: user has not yet completed their profile, 1: user can login and use
	# all features of site

	def __str__(self):
		myList = ["Name: " + self.user.first_name + " " + self.user.last_name, \
					"Sharezone: " + self.sharezone]
		return ",".join(myList)


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

	preferences_Privacy = models.IntegerField(default=-1)				
	#public: 0 - Open anyone can see the shed and borrow from it. Request to join is accepted automaticly
		#NonMemberview - anyone in community can see, tools,members,address
		#joining   	   - Request is accepted automaticly

	#private 1 - Open to only people who have been authorized, See name,owner,number of members,number of tools but no particulars like specific tools,users
		#NonMemberView - anyone in community can see, number of members, number of tools
		#joining       - Request to join must be aproved by a shed admin

	#secret  2 - no one can see the shed even exists but people who have been invited to it
		#NonMemberView - no one that is not a shed member is even aware of this shed.
		#joining 	   - Join is only on invite by a shed admin

	preferences_MinumumReputation = models.IntegerField(default=-1) # this only applies to public sheds





	def __str__(self):
		myList = ["Name: " + self.name, "Sharezone: " + self.sharezone, \
						"Owned by " + self.owner.user.username]
		return ",".join(myList)

class Tool(models.Model):
	timeCreated = models.DateTimeField(auto_now_add=True)
	timeLastEdited = models.DateTimeField(auto_now_add=True)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	tags = models.CharField(max_length=200) #categories that apply to this tool object
	owner = models.ForeignKey('Profile', related_name='ownerOfTool') #the Profile who owns this tool
	borrower = models.ForeignKey('Profile',null=True, related_name='borrowerOfTool') # the Profile who is borrowing the tool
	myShed = models.ForeignKey('Shed',null=True) #the Shed this tool is apart of
	location = models.CharField(max_length=75) #current location of the tool
	#picture = models.FileField(upload_to='documents/%Y/%m/%d')    WILL REPLACE PICTURE WHEN FRONT END CREATED
	condition = models.IntegerField(default=0) #0-10 scale
	isAvailable = models.BooleanField()
	borrowedCount = models.IntegerField(default=0) # times Tool borrowed
	requestedCount = models.IntegerField(default=0) # times Tool requested
	preferences = models.CharField(max_length=50) #serialized JSON object

	preferences_Default_MaxBorrowTime = models.IntegerField(default=30) #time measured in days only 
	#applies to tools if free to borrow is enabled 
	#0 means unlimited time

	preferences_DefaultFreeToBorrow = models.IntegerField(default=0)  
	#0 means borrow request accepted automaticly
	#1 means aproval of borrow request required

	preferences_MinimumReputation = models.IntegerField(default=0) 
	#if free to borrow enabled this states the minimum reputation of a person who can borrow the tool 



	def __str__(self):
		myList = ["Name: " + self.name, "Owned by " + self.owner.user.username, \
					"Borrowed by" + self.borrower, "My shed: " + self.myShed.name]
		return ",".join(myList)


class Notification(models.Model):
	content = models.CharField(max_length=50) #serialized JSON object


class Action(models.Model):
	content = models.CharField(max_length=50) #serialized JSON object
