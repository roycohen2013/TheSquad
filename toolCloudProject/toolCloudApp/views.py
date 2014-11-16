from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
import django.db
from toolCloudApp.models import Profile, User, Notification, Action
from toolCloudApp.mailSend import sendMail
import string
import random

"""
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1,parentdir) 
"""
import utilities.profileUtilities as profileUtil
import utilities.shedUtilities as shedUtil
import utilities.toolUtilities as toolUtil
import utilities.notificationUtilities as notifUtil
import utilities.actionUtilities as actionUtil
import utilities.content as content

def home(request):
    file = open("homePageText.txt","r")
    strings = file.readlines()
    context = {}
    context['strings'] = strings
    context.update(content.genContent(request))
    if request.user.is_anonymous():
        return render(request, 'loggedOutBase.html', context)
    return HttpResponseRedirect('/accounts/loggedin')

#Import a user registration form
from toolCloudApp.forms import UserRegistrationForm, ToolCreationForm, ShedCreationForm


# User Register View
def user_register(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                #send confirmation email
                #sendMail(form.cleaned_data['email'],"Welcome to ToolCloud! ", "Hi " + form.cleaned_data['first_name'] + ", \n\nThank you for registering with ToolCloud. \n\nLove, \n\nThe Squad")
                context = {}
                context['name'] = form.cleaned_data['username']
                return render_to_response('register_success.html', context)
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
        #add message flag that will display to user "you must be logged in to..."
        return HttpResponseRedirect('/accounts/login/') #redirect to login page
    else:
        if request.method == 'POST':
            form = ToolCreationForm(request.user, request.POST)
            if form.is_valid():
                tool = form.save()
                tool.save()

                # while (True):
                #     try:
                #         tool.toolID = ''.join(random.choice(string.ascii_letters) for i in range(8))
                #         tool.save()
                #     except django.db.IntegrityError:
                #         continue
                #     break
                #send email
                #sendMail(request.user.email, "Your Tool Submission Has Been Accepted! ", "Hey there " + request.first_name + ", \n\nThanks for submitting your " + form.cleaned_data['name'] + " to ToolCloud.  We'll let you know when someone wants to borrow it. \n\nCheers, \n\nThe Squad")
                context = {}
                context['name'] = form.cleaned_data['name']
                return render_to_response('submission_success.html', context)
        else:
            form = ToolCreationForm(request.user)
        context = {}
        context.update(csrf(request))
        context['form'] = form
        return render_to_response('tool_creation.html', context)


#a view that allows the user to see their profile
def view_profile(request, username=None):
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        #add message flag that will display to user "you must be logged in to..."
        return HttpResponseRedirect('/accounts/login/') #redirect to login page
    else:
        if request.method == 'POST':
            if username is not None:
                try:
                    userProfile = profileUtil.getProfileFromUser(User.objects.get(username=username))
                except ObjectDoesNotExist:
                    return render_to_response("profile_dne.html")
            else:
                userProfile = profileUtil.getProfileFromUser(request.user)
            toolsOwned = toolUtil.getAllToolsOwnedBy(userProfile)
            toolsBorrowed = toolUtil.getAllToolsBorrowedBy(userProfile)
            profilesInShareZone = profileUtil.getAllOtherProfilesInShareZone(userProfile)
        else:
            if username is not None:
                try:
                    userProfile = profileUtil.getProfileFromUser(User.objects.get(username=username))
                except ObjectDoesNotExist:
                    return render_to_response("profile_dne.html")
            else:
                userProfile = profileUtil.getProfileFromUser(request.user)
            toolsOwned = toolUtil.getAllToolsOwnedBy(userProfile)
            toolsBorrowed = toolUtil.getAllToolsBorrowedBy(userProfile)
            profilesInSharezone = profileUtil.getAllOtherProfilesInSharezone(userProfile)
            sheds = shedUtil.getAllShedsJoinedBy(userProfile)
        context = {}
        context.update(csrf(request))
        context['currentUser'] = request.user
        context['userProfile'] = userProfile
        context['toolsOwned'] = toolsOwned
        context['toolsBorrowed'] = toolsBorrowed
        context['profilesInSharezone'] = profilesInSharezone
        context['sheds'] = sheds
        return render_to_response('view_profile.html', context)

def view_current_profile(request):
    """this view redirects accounts/profile to the profile of the current logged in user
    """
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        return HttpResponseRedirect('/accounts/login/') #redirect to login page
    else:
        username = request.user.username
        print(' ')
        return HttpResponseRedirect(reverse('profile', args=(username,))) #comma for args to make string not look like a list of characters

#a view that will allow us to see an individual tool
def view_tool_page(request, id):
    if request.user.is_anonymous():
        #tell user they need to be logged in to that
        #add message flag that will display to user "you must be logged in to..."
        return HttpResponseRedirect('/accounts/login') #redirect to login page
    else:
        if request.method == 'POST':
            if id is not None:
                try:
                    toolObj = toolUtil.getToolFromID(id)
                except ObjectDoesNotExist:
                    return render_to_response("tool_dne.html")
            else:
                return HttpResponseRedirect('/tools/toolnotfound') #redirect to tool not found page
            owner = toolUtil.getToolOwner(toolObj)
            name = toolUtil.getToolName(toolObj)
            description = toolUtil.getToolDescription(toolObj)
            tags = toolUtil.getToolTags(toolObj)
            borrower = toolUtil.getToolBorrower(toolObj)
            condition = toolUtil.getToolCondition(toolObj)
            available = toolUtil.isToolAvailable(toolObj)
        else:
            if id is not None:
                try:
                    toolObj = toolUtil.getToolFromID(id)
                except ObjectDoesNotExist:
                    return render_to_response("tool_dne.html")
            else:
                return HttpResponseRedirect('/tools/toolnotfound') #redirect to tool not found page
            owner = toolUtil.getToolOwner(toolObj)
            name = toolUtil.getToolName(toolObj)
            description = toolUtil.getToolDescription(toolObj)
            tags = toolUtil.getToolTags(toolObj)
            borrower = toolUtil.getToolBorrower(toolObj)
            condition = toolUtil.getToolCondition(toolObj)
            available = toolUtil.isToolAvailable(toolObj)
            if profileUtil.getProfileFromUser(request.user) == owner:
                ownedByUser = True
            else:
                ownedByUser = False
        context = {}
        context.update(csrf(request))
        context['tool'] = toolObj
        context['name'] = name
        context['owner'] = owner
        context['description'] = description
        context['tags'] = tags
        context['borrower'] = borrower
        context['condition'] = condition
        context['available'] = available
        context['ownedByUser'] = ownedByUser
        return render_to_response('tool_page.html', context)
     
def view_shed_page(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect("/accounts/login")
    else:
        if id is not None:
            try:
                shedObj = shedUtil.getShedFromID(id)
            except ObjectDoesNotExist:
                return render_to_response("shed_dne.html")
        else:
            return render_to_response("shed_dne.html")
        owner = shedUtil.getOwnerOfShed(shedObj)
        name = shedUtil.getNameOfShed(shedObj)
        admins = shedUtil.getAllAdminsOfShed(shedObj)
        members = shedUtil.getAllMembersOfShed(shedObj)
        tools = toolUtil.getAllToolsInShed(shedObj)
        userProfile = profileUtil.getProfileFromUser(request.user)
        meetsMinRep = userProfile.reputation >= shedObj.minimumReputation
        shedMembership = shedUtil.checkForMembership(userProfile, id)
        context = {}
        context.update(csrf(request))
        context['owner'] = owner
        context['name'] = name
        context['admins'] = admins
        context['members'] = members
        context['tools'] = tools
        context['meetsMin'] = meetsMinRep
        context['alreadyMember'] = shedMembership
        return render_to_response('shed_page.html', context)

#a view that will display all tools
def all_tools(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        tools = toolUtil.getAllTools()
        context = {}
        context.update(csrf(request))
        context['tools'] = tools
        return render_to_response('all_tools.html', context)

def borrow_tool(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        borrowerProfile = profileUtil.getProfileFromUser(request.user)
        toolObject = toolUtil.getToolFromID(id)
        ownerProfile = toolObject.owner
        content = borrowerProfile.user.username + " has requested to borrow your " + toolObject.name + "."
        content = content + ",Accept,Deny"                                                                  #adding questions
        actionObject = actionUtil.createBorrowRequestAction(toolObject, borrowerProfile)
        notifObject = notifUtil.createResponseNotif(toolObject, ownerProfile, content)
        notifObject.save()
        return HttpResponseRedirect('/tools/request_sent')

def request_sent(request):
    return render_to_response("request_sent.html")

def all_sheds(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        allSheds = shedUtil.getAllShedsAllSharezones()
        shedsInMySharezone = shedUtil.getAllShedsInSharezone(userProfile.sharezone)
        adminSheds = shedUtil.getAllShedsAdministratedBy(userProfile)
        ownedSheds = shedUtil.getAllShedsOwnedBy(userProfile)
        memberSheds = shedUtil.getAllShedsJoinedBy(userProfile)
        context = {}
        context.update(csrf(request))
        context['sheds'] = allSheds
        context['adminSheds'] = adminSheds
        context['ownedSheds'] = ownedSheds
        context['mySheds'] = memberSheds
        return render_to_response('all_sheds.html', context)

#a view for if a tool does not exist
def tool_dne(request):
    return render_to_response('tool_dne.html')

	
#a view for the creation of a new Shed
def create_tool_shed(request):
	if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        #add message flag that will display to user "you must be logged in to..."
		return HttpResponseRedirect('/accounts/login/') #redirect to login page
	else:
		if request.method == 'POST':
			form = ShedCreationForm(request.user, request.POST)
			
			if form.is_valid():
				shed = form.save()
                #send email
                #sendMail(request.user.email, "Your Tool Submission Has Been Accepted! ", "Hey there " + request.first_name + ", \n\nThanks for submitting your " + form.cleaned_data['name'] + " to ToolCloud.  We'll let you know when someone wants to borrow it. \n\nCheers, \n\nThe Squad")
				context = {}
				context['name'] = form.cleaned_data['name']
				return render_to_response('shed_registration_success.html', context)
		else:
			form = ShedCreationForm(request.user)
		context = {}
		context.update(csrf(request))
		context['form'] = form
		return render_to_response('shed_creation.html', context)

def about_us(request):
    return render_to_response('about_us.html')

#DO NOT TOUCH - team leader
def spooked(request):
    return render_to_response('spoopy.html')

def spooky(request):
    return render_to_response('spagett.html')