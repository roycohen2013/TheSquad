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

"""This form will create a new user and linked profile

written by Jackson
"""

STATE_CHOICES = [ \
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
        ]

CONDITION_CHOICES = [ \
    (1, 'Filthy'), \
    (2, 'Not the best'), \
    (3, 'Average'), \
    (4, 'Good looking'), \
    (5, 'Superb') \
    ]

STATE_DICT = dict(STATE_CHOICES)

CONDITION_DICT = dict(CONDITION_CHOICES)

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(required = True)
    street_address = forms.CharField(required = True)
    city = forms.CharField(required = True)
    state = forms.ChoiceField(choices = STATE_CHOICES, required = True, initial=STATE_CHOICES[31][0])
    zip_code = forms.CharField(required = True)
    email_notifications = forms.BooleanField(help_text = "Disable this if you do not want to receive emails from ToolCloud.", \
        initial = True)
    text_notifications = forms.BooleanField(help_text = "Disable this if you do not want to receive texts from ToolCloud.", \
        initial = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(UserRegistrationForm, self).save(commit = False)
        newProfile = Profile()
        newProfile.phoneNumber = self.cleaned_data['phone_number']
        newProfile.streetAddress = self.cleaned_data['street_address']
        newProfile.sharezone = self.cleaned_data['zip_code']
        newProfile.city = self.cleaned_data['city']
        newProfile.state = self.cleaned_data['state']
        newProfile.stateName = STATE_DICT[self.cleaned_data['state']]
        newProfile.emailNotifs = self.cleaned_data['email_notifications']
        newProfile.textNotifs = self.cleaned_data['text_notifications']
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

class UserEditForm(ModelForm):

    def __init__(self, profile, *args, **kwargs):
        self.profileObject = profile
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(required= True, initial=self.profileObject.user.first_name)
        self.fields['last_name'] = forms.CharField(required= True, initial=self.profileObject.user.last_name)
        self.fields['email'] = forms.EmailField(required= True, initial=self.profileObject.user.email)
        self.fields['phone_number'] = forms.CharField(required= True, initial=self.profileObject.phoneNumber)
        self.fields['street_address'] = forms.CharField(required = True, initial=self.profileObject.streetAddress)
        self.fields['city'] = forms.CharField(required = True, initial=self.profileObject.city)
        self.fields['state'] = forms.ChoiceField(choices = STATE_CHOICES, required = True, \
            initial=STATE_CHOICES[STATE_CHOICES.index((self.profileObject.state, self.profileObject.stateName))][0])
        self.fields['zip_code'] = forms.CharField(required = True, initial=self.profileObject.sharezone)
        self.fields['email_notifications'] = forms.BooleanField(help_text = \
            "Disable this if you do not want to receive emails from ToolCloud.", \
        initial = True)
        self.fields['text_notifications'] = forms.BooleanField(help_text =  \
            "Disable this if you do not want to receive texts from ToolCloud.", \
        initial = True)
    class Meta:
        model = User
        fields = ()

    def save(self, commit = True):
        self.profileObject.user.first_name = self.cleaned_data['first_name']
        self.profileObject.user.last_name = self.cleaned_data['last_name']
        self.profileObject.user.email = self.cleaned_data['email']
        self.profileObject.phoneNumber = self.cleaned_data['phone_number']
        self.profileObject.streetAddress = self.cleaned_data['street_address']
        self.profileObject.city = self.cleaned_data['city']
        self.profileObject.state = self.cleaned_data['state']
        self.profileObject.stateName = STATE_DICT[self.cleaned_data['state']]
        self.profileObject.sharezone = self.cleaned_data['zip_code']
        self.profileObject.emailNotifs = self.cleaned_data['email_notifications']
        self.profileObject.textNotifs = self.cleaned_data['text_notifications']
        if commit:
            self.profileObject.user.save()
            self.profileObject.save()
        return self.profileObject

"""This form will create a new Tool (link to user created in views.py)

"""

class ToolCreationForm(ModelForm):
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, required=True, \
        help_text = 'The physical condition of your tool.', initial=CONDITION_CHOICES[2][0])
    maximum_borrow_time = forms.IntegerField(max_value=60, min_value=1, required=False, \
        help_text = 'The maximum number of days a user is allowed to borrow this tool. 1-60 days.', \
        initial=30)
    minimum_reputation = forms.IntegerField(max_value=100, min_value=0, required=False, \
        help_text = 'The minimum reputation required for a user to borrow this tool. 0-100.', \
        initial=0)

    def __init__(self, user, *args, **kwargs):
        self.userObject = user
        shedList = list(shedUtil.getAllShedsJoinedBy(profileUtil.getProfileFromUser(self.userObject)))
        self.shedChoiceList = []
        for shed in shedList:
            self.shedChoiceList.append((shed.id, shed.name))
        super(ToolCreationForm, self).__init__(*args, **kwargs)
        self.fields['shed'] = forms.ChoiceField(choices=self.shedChoiceList, help_text = 'The shed this tool will be a part of.')

    class Meta:
        model = Tool
        fields = ('name', 'description', 'tags')

    def save(self,commit = True):
        tool = super(ToolCreationForm, self).save(commit = False)
        tool.owner = profileUtil.getProfileFromUser(self.userObject)
        tool.timeCreated = timezone.now()
        tool.timeLastEdited = timezone.now()
        tool.condition = self.cleaned_data['condition']
        tool.conditionReadable = CONDITION_DICT[int(self.cleaned_data['condition'])]
        tool.maxBorrowTime = self.cleaned_data['maximum_borrow_time']
        tool.minimumReputation = self.cleaned_data['minimum_reputation']
        tool.isAvailable = 1
        tool.myShed = shedUtil.getShedFromID(self.cleaned_data['shed'])
        tool.location = shedUtil.getLocationOfShed(tool.myShed)
        tool.picture = ''
        tool.borrowedCount = 0
        tool.requestedCount = 0
        tool.preferences = ''
        if commit:
            tool.save()
        return tool

class ToolEditForm(ModelForm):

    def __init__(self, tool, *args, **kwargs):
        self.toolObject = tool
        self.profileObject = self.toolObject.owner
        shedList = list(shedUtil.getAllShedsJoinedBy(self.profileObject))
        self.shedChoiceList = []
        for shed in shedList:
            self.shedChoiceList.append((shed.id, shed.name))
        super(ToolEditForm, self).__init__(*args, **kwargs)
        self.fields['name_'] = forms.CharField(required= True, initial=self.toolObject.name)
        self.fields['description_'] = forms.CharField(required= True, initial=self.toolObject.description)
        self.fields['tags_'] = forms.CharField(required= False, initial=self.toolObject.tags)
        self.fields['condition'] = forms.ChoiceField(choices = CONDITION_CHOICES, required = True, \
            initial=CONDITION_CHOICES[CONDITION_CHOICES.index((self.toolObject.condition, self.toolObject.conditionReadable))][0])
        self.fields['maximum_borrow_time'] = forms.IntegerField(max_value=60, min_value=1, required=False, \
        help_text = 'The maximum number of days a user is allowed to borrow this tool. 1-60 days.', \
        initial=self.toolObject.maxBorrowTime)
        self.fields['minimum_reputation'] = forms.IntegerField(max_value=100, min_value=0, required=False, \
        help_text = 'The minimum reputation required for a user to borrow this tool. 0-100.', \
        initial=self.toolObject.minimumReputation)
        self.fields['shed'] = forms.ChoiceField(choices=self.shedChoiceList, \
            initial=self.shedChoiceList[self.shedChoiceList.index((self.toolObject.myShed.id, self.toolObject.myShed.name))][0],\
            help_text = 'The shed this tool will be a part of.')

    class Meta:
        model = Tool
        fields = ()

    def save(self, commit = True):
        self.toolObject.name = self.cleaned_data['name_']
        self.toolObject.description = self.cleaned_data['description_']
        self.toolObject.tags = self.cleaned_data['tags_']
        self.toolObject.condition = self.cleaned_data['condition']
        self.toolObject.conditionReadable = CONDITION_DICT[int(self.cleaned_data['condition'])]
        self.toolObject.maxBorrowTime = self.cleaned_data['maximum_borrow_time']
        self.toolObject.minimumReputation = self.cleaned_data['minimum_reputation']
        self.toolObject.myShed = shedUtil.getShedFromID(self.cleaned_data['shed'])
        self.profileObject.location = shedUtil.getShedFromID(self.cleaned_data['shed']).location
        if commit:
            self.toolObject.save()
        return self.toolObject 

"""
This form will create a new Shed
""" 
class ShedCreationForm(ModelForm):
    minimum_reputation = forms.IntegerField(max_value=100, min_value=0, required=False, \
        help_text = 'The minimum reputation required for a user to join this shed. 0-100.', \
        initial=0)

    def __init__(self, user, *args, **kwargs):
        self.userObject = user
        self.profileObject = profileUtil.getProfileFromUser(self.userObject)
        self.userAddress = self.profileObject.streetAddress + ", " + self.profileObject.city + ", " + self.profileObject.state + \
           " " + self.profileObject.sharezone
        super(ShedCreationForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.CharField(required=False, initial=self.userAddress, \
            help_text= 'The location of the shed.  Only visible to approved members.  Edit if not your own address.')

    class Meta:
        model = Shed
        fields = ('name',)
        
    def save(self,commit = True):
        shed = super(ShedCreationForm, self).save(commit = False)
        shed.timeCreated = timezone.now()
        shed.timeLastEdited = timezone.now()
        shed.owner = self.profileObject
        shed.sharezone = self.profileObject.sharezone
        shed.minimumReputation = self.cleaned_data['minimum_reputation']
        shed.location = self.cleaned_data['location']
        #shed.latitude = ''
        #shed.longitude = ''
        #shed.status = ''
        #shed.admins = ''
        #shed.members = ''
        #shed.privacy = ''
        if commit:
            shed.save()
        return shed

class ShedEditForm(ModelForm):

    def __init__(self, shed, *args, **kwargs):
        self.shedObject = shed
        self.profileObject = self.shedObject.owner
        super(ShedEditForm, self).__init__(*args, **kwargs)
        self.fields['name_'] = forms.CharField(required=True, initial=self.shedObject.name)
        self.fields['minimum_reputation'] = forms.IntegerField(max_value=100, min_value=0, required=False, \
        help_text = 'The minimum reputation required for a user to join this shed. 0-100.', \
        initial=self.shedObject.minimumReputation)
        self.fields['location_'] = forms.CharField(required=False, initial=self.shedObject.location, \
            help_text= 'The location of the shed.  Only visible to approved members.  Edit if not your own address.')

    class Meta:
        model = Shed
        fields = ()

    def save(self, commit = True):
        self.shedObject.name = self.cleaned_data['name_']
        self.shedObject.minimumReputation = self.cleaned_data['minimum_reputation']
        self.shedObject.location = self.cleaned_data['location_']
        if commit:
            self.shedObject.save()
        return self.shedObject

class debugForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    a = forms.CharField(widget = forms.Textarea)
    #All my attributes here
    
class passwordResetForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    password = forms.CharField(required = True, widget=forms.PasswordInput())
    confirm_password = forms.CharField(required = True, widget=forms.PasswordInput())
    #All my attributes here
    