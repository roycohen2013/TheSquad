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
import utilities.extraUtilities, utilities.profileUtilities, utilities.shedUtilities, utilities.toolUtilities

def home(request):
	return render(request, 'base.html')

#Import a user registration form
from toolCloudApp.forms import UserRegistrationForm, ToolCreationForm

# User Login View
def user_login(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            #This authenticates the user
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    #This logs him in
                    login(request, user)
                else:
                    return HttpResponse("Not active")
            else:
                return HttpResponse("Wrong username/password")
    return render(request, 'myapp/login_error.html')
    


    #return HttpResponseRedirect("/")

# User Logout View
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

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
            form = ToolCreationForm(request.POST)
            if form.is_valid:
                tool = form.save()
                tool.ownerID = profileUtilities.getProfileFromUser(request.user)
                tool.save()
                #send email
                #sendMail(request.user.email, "Your Tool Submission Has Been Accepted! ", "Hey there " + request.first_name + ", \n\nThanks for submitting your " + form.cleaned_data[] + " to ToolCloud.  We'll let you know when someone wants to borrow it. \n\nCheers, \n\nThe Squad")
                return HttpResponse('Tool submitted successfully.')
        else:
            form = ToolCreationForm()
        context = {}
        context.update(csrf(request))
        conext['form'] = form
        return render_to_response('tool_creation.html', context)
