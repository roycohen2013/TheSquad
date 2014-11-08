"""
    Our database tables.
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic



"""
    The Profile class is an extension of Django's User class
    and stores basic account information.
"""
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='myProfile')

    timeCreated = models.DateTimeField(auto_now_add=True)
    phoneNumber = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    sharezone = models.CharField(max_length=5) #five digit zip code
    status = models.CharField(max_length=50)
    #picture = models.FileField(upload_to='documents/%Y/%m/%d')
    reputation = models.IntegerField(default=50) #0..100 rating

    preferences_Privacy = models.IntegerField(default=0)
    #public   0 - you can see everything 
    #private 1 - persons name
    #secret  2 - initials

    content_type = models.ForeignKey(ContentType,null=True,blank=True)
    object_id = models.PositiveIntegerField(null=True,default=1)

    #registered = models.IntegerField(default=0) #0: user has not yet completed their profile, 1: user can login and use
    # all features of site

    """
        ToString method.
    """
    def __str__(self):
        myList = ["Name: " + self.user.first_name + " " + self.user.last_name, \
                    "Sharezone: " + self.sharezone]
        return ",".join(myList)

    """
        Overrides save to work with generic notifications.
    """
    def save(self, *args, **kwargs):
        #do_something()
        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method.
        self.object_id = self.id
        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method.
        #do_something_else()



"""
    The Shed class stores all information about a particular shed
    including all its members, admins, etc.
"""
class Shed(models.Model):
    owner = models.ForeignKey('Profile',related_name='mySheds') #the Profile who owns this shed (sueprAdmin)
    admins = models.ManyToManyField('Profile',related_name='adminOfShed',null=True) #admins of shed
    members = models.ManyToManyField('Profile',related_name='memberOfShed',null=True) #members of shed

    timeCreated = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=75) #address of the shed
    sharezone = models.CharField(max_length=5) #five digit zip code
    latitude = models.IntegerField(default=-1)
    longitude = models.IntegerField(default=-1)
    status = models.CharField(max_length=50)
    #picture = models.FileField(upload_to='documents/%Y/%m/%d')

    content_type = models.ForeignKey(ContentType,null=True,blank=True) # for generic notifications
    object_id = models.PositiveIntegerField(null=True,default=1) # for generic notifications


    privacy = models.IntegerField(default=-1)               
    #public: 0 - Open anyone can see the shed and borrow from it. Request to join is accepted automaticly
        #NonMemberview - anyone in community can see, tools,members,address
        #joining       - Request is accepted automaticly

    #private 1 - Open to only people who have been authorized, See name,owner,number of members,number of
    #            tools but no particulars like specific tools,users
        #NonMemberView - anyone in community can see, number of members, number of tools
        #joining       - Request to join must be aproved by a shed admin

    #secret  2 - no one can see the shed even exists but people who have been invited to it
        #NonMemberView - no one that is not a shed member is even aware of this shed.
        #joining       - Join is only on invite by a shed admin

    minimumReputation = models.IntegerField(default=-1) # this only applies to public sheds

    """
        ToString method.
    """
    def __str__(self):
        myList = ["Name: " + self.name, "Sharezone: " + self.sharezone, \
                        "Owned by " + self.owner.user.username]
        return ",".join(myList)

    """
        Overrides save to work with generic notifications.
    """
    def save(self, *args, **kwargs):
        #do_something()
        super(Shed, self).save(*args, **kwargs) # Call the "real" save() method.
        self.object_id = self.id
        #print (content_type)
        super(Shed, self).save(*args, **kwargs) # Call the "real" save() method.
        #do_something_else()



"""
    The Tool class stores all information about tools including its owner,
    borrower, shed, etc.
"""
class Tool(models.Model):
    owner = models.ForeignKey('Profile', related_name='toolsOwned') #the Profile who owns this tool
    borrower = models.ForeignKey('Profile',null=True, related_name='toolsBorrowed') # the Profile who is borrowing the tool
    myShed = models.ForeignKey('Shed',null=True,related_name='toolsInShed') #the Shed this tool is apart of

    timeCreated = models.DateTimeField(auto_now_add=True)
    timeLastEdited = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)#categories that apply to this tool object
    location = models.CharField(max_length=75) #current location of the tool
    #picture = models.FileField(upload_to='documents/%Y/%m/%d')
    condition = models.IntegerField(default=0) #0-10 scale
    isAvailable = models.BooleanField()
    borrowedCount = models.IntegerField(default=0) # times Tool borrowed
    requestedCount = models.IntegerField(default=0) # times Tool requested

    defaultMaxBorrowTime = models.IntegerField(default=30)#time measured in days only
    #applies to tools if free to borrow is enabled 
    #0 means unlimited time

    defaultFreeToBorrow = models.IntegerField(default=0)#preferences
    #0 means borrow request accepted automaticly
    #1 means aproval of borrow request required

    minimumReputation = models.IntegerField(default=0)#preferences
    #if free to borrow enabled this states the minimum reputation of a person who can borrow the tool 

    content_type = models.ForeignKey(ContentType,null=True,blank=True) # for generic notifications
    object_id = models.PositiveIntegerField(null=True,default=1) # for generic notifications

    """
        ToString method.
    """
    def __str__(self):
        myList = ["Name: " + self.name, "Owned by " + self.owner.user.username, \
                    "Borrowed by" + self.borrower, "My shed: " + self.myShed.name]
        return ",".join(myList)

    """
        Overrides save to work with generic notifications.
    """
    def save(self, *args, **kwargs):
        #do_something()
        super(Tool, self).save(*args, **kwargs) # Call the "real" save() method.
        
        self.object_id = self.id
        super(Tool, self).save(*args, **kwargs) # Call the "real" save() method.
        #do_something_else()



"""
    Provides functionality for notifications.
"""
class Notification(models.Model):
    
    content_type = models.ForeignKey(ContentType,null=True,blank=True) # for generic notifications
    object_id = models.PositiveIntegerField(null=True,default=1) # for generic notifications
    #ContentType.objects.get_for_model(self)

    recipient = models.ForeignKey('Profile', related_name='myNotifications',null=True)#reciever of notification
    source = generic.GenericForeignKey('content_type', 'object_id')#action that caused it

    content = models.CharField(max_length=280,null=True)
    #if type == info: content is string of text
    #elif type == request: content is
        #-multiple choice - question, then choices in CSV form
        #-open ended - user prompt text
    notificationType = models.CharField(max_length="20",null=True)#type of notification can be either "info" or "request" ex. TCP vs UDP
    timestamp = models.DateTimeField(auto_now_add=True,null=True)

    response = models.CharField(max_length="40",null=True)#Starts off being null. when filled out the notification has been responded to

    """
        Overrides save to work with generic notifications.
    """
    def save(self, *args, **kwargs):
        #do_something()
        super(Notification, self).save(*args, **kwargs) # Call the "real" save() method.
        self.object_id = self.id
        super(Notification, self).save(*args, **kwargs) # Call the "real" save() method.
        #do_something_else()



"""
    Works with the Notification class to handle notifications.
"""
class Action(models.Model):
    tool = models.ForeignKey('Tool', related_name='toolActions')#if tool, send to owner of tool
    shed = models.ForeignKey('Shed', related_name='shedActions')#if shed, send to all admins of shed
    admin = models.ForeignKey('Profile', related_name='adminActions')#returns list of actions that a user is controlling of
    requester = models.ForeignKey('Profile', related_name='requesterActions')

    actionType = models.CharField(max_length=20)#either tool, or shed
    currrentState = models.CharField(max_length=20)
    timestamps = models.CharField(max_length=560)#CSV timestamps for every state
    workSpace = models.CharField(max_length=200)#for use in state machine

    content_type = models.ForeignKey(ContentType,null=True,blank=True)
    object_id = models.PositiveIntegerField(null=True,default=1)

    """
        Overrides save to work with generic notifications.
    """
    def save(self, *args, **kwargs):
        #do_something()
        super(Action, self).save(*args, **kwargs) # Call the "real" save() method.
        self.object_id = self.id
        super(Action, self).save(*args, **kwargs) # Call the "real" save() method.
        #do_something_else()
