from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from toolCloudApp.models import Profile
from toolCloudApp.mailSend import sendMail
"""
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1,parentdir) 
"""
import utilities.extraUtilities as extraUtil, utilities.profileUtilities as profileUtil, utilities.shedUtilities as shedUtil, utilities.toolUtilities as toolUtil
import utilities.content as content

def home(request):
    return render(request, 'base.html', content.genContent(request))

#Import a user registration form
from toolCloudApp.forms import UserRegistrationForm, ToolCreationForm


# User Register View
def user_register(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid:
                form.save()
                #send confirmation email
                #sendMail(form.cleaned_data['email'],"Welcome to ToolCloud! ", "Hi " + form.cleaned_data['first_name'] + ", \n\nThank you for registering with ToolCloud. \n\nLove, \n\nThe Squad")
                return HttpResponse('User created succcessfully.')
        else:
            form = UserRegistrationForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        #Pass the context to a template
        return render_to_response('register.html', context)
    else:
        return HttpResponseRedirect('/')

# Tool Submission View
def tool_submission(request):
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        return HttpResponseRedirect('/') #redirect to login page
    else:
        if request.method == 'POST':
            form = ToolCreationForm(request.user, request.POST)
            if form.is_valid:
                form.save()
                #send email
                #sendMail(request.user.email, "Your Tool Submission Has Been Accepted! ", "Hey there " + request.first_name + ", \n\nThanks for submitting your " + form.cleaned_data['name'] + " to ToolCloud.  We'll let you know when someone wants to borrow it. \n\nCheers, \n\nThe Squad")
                return HttpResponse('Tool submitted successfully.')
        else:
            form = ToolCreationForm(request.user)
        context = {}
        context.update(csrf(request))
        context['form'] = form
        return render_to_response('tool_creation.html', context)

def view_profile(request):
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        return HttpResponseRedirect('/') #redirect to login page
    else:
        if request.method == 'POST':
            username = request.user.username
            userProfile = profileUtil.getProfileFromUser(request.user)
            toolsOwned = toolUtil.getAllToolsOwnedBy(userProfile)
            toolsBorrowed = toolUtil.getAllToolsBorrowedBy(userProfile)
            profilesInShareZone = profileUtil.getAllProfilesInShareZone(profileUtil.getShareZone(userProfile))
        else:
            pass
        context = {}
        context.update(crsf(request))
        context['username'] = username
        context['userProfile'] = userProfile
        context['toolsOwned'] = toolsOwned
        context['toolsBorrowed'] = toolsBorrowed
        context['profilesInShareZone'] = profilesInShareZone
        return render_to_response('view_profile.html', context)