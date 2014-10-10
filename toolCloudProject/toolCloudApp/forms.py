"""
$LastChangedDate: $
$Rev: $
$Author: $

"""

from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from toolCloudApp.models import Profile
from django.utils import timezone

"""This form will create a new user and linked profile

written by Jackson
"""

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(required = True)
    share_zone = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')        

    def save(self,commit = True):   
        user = super(UserRegistrationForm, self).save(commit = False)
        newProfile = Profile()
        newProfile.phoneNumber = self.cleaned_data['phone_number']
        newProfile.sharezone = self.cleaned_data['share_zone']
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
