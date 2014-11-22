"""
$LastChangedDate: $
$Rev: $
$Author: $

"""

"""This file contains all forms for User, Profile, Tool, and shed creation.

"""
from django import forms
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from toolCloudApp.models import Profile, Tool, Shed
from django.utils import timezone
import utilities.profileUtilities as profileUtil, utilities.shedUtilities as shedUtil, utilities.toolUtilities as toolUtil
import utilities.content as content
import string
import random

"""This form will create a new user and linked profile

written by Jackson
"""

class UserRegistrationForm(UserCreationForm):
    STATE_CHOICES = ( \
        ('AL','Alabama'), \
        ('AK', 'Alaska'), \
        ('AZ', 'Arizona'), \
        ('AR', 'Arkansas'), \
        ('CA', 'California'), \
        ('CO', 'Colorado'), \
        ('CT', 'Connecticut'), \
        ('DE', 'Delaware'), \
        ('FL', 'Florida'), \
        ('GA', 'Georgia'), \
        ('HI', 'Hawaii'), \
        ('IH', 'Idaho'), \
        ('IL', 'Illinois'), \
        ('IN', 'Indiana'), \
        ('IA', 'Iowa'), \
        ('KS', 'Kansas'), \
        ('KY', 'Kentucky'), \
        ('LA', 'Louisiana'), \
        ('ME', 'Maine'), \
        ('MD', 'Maryland'), \
        ('MA', 'Massachusetts'), \
        ('MI', 'Michigan'), \
        ('MN', 'Minnesota'), \
        ('MI', 'Mississippi'), \
        ('MO', 'Missouri'), \
        ('MT', 'Montana'), \
        ('NE', 'Nebraska'), \
        ('NV', 'Nevada'), \
        ('NH', 'New Hampshire'), \
        ('NJ', 'New Jersey'), \
        ('NM', ' New Mexico'), \
        ('NY', 'New York'), \
        ('NC', 'North Carolina'), \
        ('ND', 'North Dakota'), \
        ('OH', 'Ohio'), \
        ('OK', 'Oklahoma'), \
        ('OR', 'Oregon'), \
        ('PA', 'Pennsylvania'), \
        ('RI', 'Rhode Island'), \
        ('SC', 'South Carolina'), \
        ('SD', 'South Dakota'), \
        ('TN', 'Tennessee'), \
        ('TX', 'Texas'), \
        ('UT', 'Utah'), \
        ('VT', 'Vermont'), \
        ('VA', 'Virginia'), \
        ('WA', 'Washington'), \
        ('WV', 'West Virginia'), \
        ('WI', 'Wisconsin'), \
        ('WY', 'Wyoming') \
        )
    phone_number = forms.CharField(required = True)
    street_address = forms.CharField(required = True)
    city = forms.CharField(required = True)
    state = forms.ChoiceField(choices = STATE_CHOICES, required = True)
    zip_code = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(UserRegistrationForm, self).save(commit = False)
        newProfile = Profile()
        newProfile.phoneNumber = self.cleaned_data['phone_number']
        newProfile.streetAddress = self.cleaned_data['street_address']
        newProfile.sharezone = self.cleaned_data['zip_code']
        newProfile.state = self.cleaned_data['state']
        newProfile.picture = ''
        newProfile.status = ''
        newProfile.reputation = 50
        newProfile.preferences = ''
        newProfile.timeCreated = timezone.now()
        if commit:
            user.save()
            newProfile.user = user
            newProfile.save()
        return user

"""This form will create a new Tool (link to user created in views.py)

"""

class ToolCreationForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.userObject = user
        super(ToolCreationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tool
        fields = ('name', 'description', 'tags', 'condition')

    def save(self,commit = True):
        tool = super(ToolCreationForm, self).save(commit = False)
        #tool.toolID = ''.join(random.choice(string.ascii_letters) for i in range(7))
        tool.timeCreated = timezone.now()
        tool.timeLastEdited = timezone.now()
        tool.owner = profileUtil.getProfileFromUser(self.userObject)
        tool.isAvailable = 1
        tool.location = ''
        tool.picture = ''
        tool.borrowedCount = 0
        tool.requestedCount = 0
        tool.preferences = ''
        tool.myShed = None
        if commit:
            tool.save()
        return tool
    
"""
This form will create a new Shed
""" 
class ShedCreationForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        self.userObject = user
        super(ShedCreationForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Shed
        fields = ('name', 'sharezone', 'minimumReputation')
        
    def save(self,commit = True):
        shed = super(ShedCreationForm, self).save(commit = False)
        shed.timeCreated = timezone.now()
        shed.timeLastEdited = timezone.now()
        shed.owner = profileUtil.getProfileFromUser(self.userObject)
        #shed.location = ''
        #shed.latitude = ''
        #shed.longitude = ''
        #shed.status = ''
        #shed.admins = ''
        #shed.members = ''
        #shed.privacy = ''
        if commit:
            shed.save()
        return shed

class debugForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    a = forms.CharField(widget = forms.Textarea)
    #All my attributes here