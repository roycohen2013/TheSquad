from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
import django.db
from toolCloudApp.models import Profile, Tool, Shed, User, Notification, Action
from toolCloudApp.mailSend import sendMail
from datetime import datetime
import string
import random
#import toolCloudApp.stateMachines.actionManager

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
    context.update(content.genSuper())
    if request.user.is_anonymous():
        return render(request, 'loggedOutBase.html', context)
    return render_to_response('userHome.html', content.genUserHome(request))

#Import a user registration form
from toolCloudApp.forms import UserRegistrationForm, ToolCreationForm, ShedCreationForm


# User Register View
def user_register(request):
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                userAccount = form.save()
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                if user is not None:
                    login(request, user)
                #send confirmation email
                #sendMail(form.cleaned_data['email'],"Welcome to ToolCloud! ", "Hi " + form.cleaned_data['first_name'] + ", \n\nThank you for registering with ToolCloud. \n\nLove, \n\nThe Squad")
                shedName = form.cleaned_data['username'] + "'s Shed"
                userProfile = profileUtil.getProfileFromUser(userAccount)
                newShedObject = Shed(name=shedName, owner=userProfile, location='location', sharezone=form.cleaned_data['zip_code'],\
                    status='status')
                newShedObject.save()
                newShedObject.members.add(userProfile)
                newShedObject.admins.add(userProfile)
                newShedObject.save()
                context = {}
                context['name'] = form.cleaned_data['username']
                return render_to_response('userHome.html', context)
        else:
            form = UserRegistrationForm()
        context = {}
        context.update(csrf(request))
        context['form'] = form
        context.update(content.genSuper())
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
                #send email
                #sendMail(request.user.email, "Your Tool Submission Has Been Accepted! ", "Hey there " + request.first_name + ", \n\nThanks for submitting your " + form.cleaned_data['name'] + " to ToolCloud.  We'll let you know when someone wants to borrow it. \n\nCheers, \n\nThe Squad")
                context = {}
                context['name'] = form.cleaned_data['name']
                return render_to_response('submission_success.html', context)
        else:
            form = ToolCreationForm(request.user)
        context = {}
        context.update(csrf(request))
        context.update(content.genBaseLoggedIn(request))
        context['form'] = form
        return render_to_response('tool_creation.html', context)

def edit_tool(request, id):
    #stuff
    pass

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
                context.update(content.genBaseLoggedIn(request))
                return render_to_response('shed_registration_success.html', context)
        else:
            form = ShedCreationForm(request.user)
        context = {}
        context.update(csrf(request))
        context['form'] = form
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('shed_creation.html', context)

def edit_shed(request, id):
    #other stuff
    pass
    
#a view that allows the user to see their profile
def view_profile(request, username=None):
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        #add message flag that will display to user "you must be logged in to..."
        return HttpResponseRedirect('/accounts/login/') #redirect to login page
    else:
        if username is not None:
            try:
                userProfile = profileUtil.getProfileFromUser(User.objects.get(username=username))
            except ObjectDoesNotExist:
                context = {}
                context['object'] = 'profile'
                context.update(content.genBaseLoggedIn(request))
                return render_to_response("dne.html", context)
        else:
            userProfile = profileUtil.getProfileFromUser(request.user)
        toolsOwned = toolUtil.getAllToolsOwnedBy(userProfile)
        toolsBorrowed = toolUtil.getAllToolsBorrowedBy(userProfile)
        sheds = shedUtil.getAllShedsJoinedBy(userProfile)
        context = {}
        context.update(csrf(request))
        context['currentUser'] = request.user
        context['userProfile'] = userProfile
        context['toolsOwned'] = toolsOwned
        context['toolsBorrowed'] = toolsBorrowed
        context['sheds'] = sheds
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('view_profile.html', context)

def view_current_profile(request):
    """this view displays account information and allows users to edit their information
    """
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        return HttpResponseRedirect('/accounts/login/') #redirect to login page
    else:
        currentUser = request.user
        userProfile = profileUtil.getProfileFromUser(currentUser)
        reputation = profileUtil.getReputation(userProfile)
        timeCreated = userProfile.timeCreated
        streetAddress = profileUtil.getAddress(userProfile)
        city = profileUtil.getCity(userProfile)
        state = profileUtil.getStateName(userProfile)
        shareZone = profileUtil.getSharezone(userProfile)
        context = {}
        context.update(csrf(request))
        context['userProfile'] = userProfile
        context['timeStamp'] = timeCreated
        context['streetAddress'] = streetAddress
        context['reputation'] = reputation
        context['city'] = city
        context['state'] = state
        context['sharezone'] = shareZone
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('my_account.html', context)

#a view that will allow us to see an individual tool
def view_tool_page(request, id, contextArg):#contextArg is a dict to be added to the content dict
    if request.user.is_anonymous():
        #tell user they need to be logged in to that
        #add message flag that will display to user "you must be logged in to..."
        return HttpResponseRedirect('/accounts/login') #redirect to login page
    else:
        if id is not None:
            try:
                toolObj = toolUtil.getToolFromID(id)
            except ObjectDoesNotExist:
                context = {}
                context['object'] = 'tool'
                context.update(content.genBaseLoggedIn(request))
                return render_to_response("dne.html", context)
        else:
            return HttpResponseRedirect('/tools/toolnotfound') #redirect to tool not found page
        owner = toolUtil.getToolOwner(toolObj)
        name = toolUtil.getToolName(toolObj)
        description = toolUtil.getToolDescription(toolObj)
        tags = toolUtil.getToolTags(toolObj)
        borrower = toolUtil.getToolBorrower(toolObj)
        condition = toolUtil.getToolConditionReadable(toolObj)
        available = toolUtil.isToolAvailable(toolObj)
        if profileUtil.getProfileFromUser(request.user) == owner:
            ownedByUser = True
        else:
            ownedByUser = False
        meetsMinRep = (profileUtil.getReputation(profileUtil.getProfileFromUser(request.user)) >= toolObj.minimumReputation)
        context = {}
        context.update(csrf(request))
        context['tool'] = toolObj
        context['name'] = name #TODO change to toolName
        context['owner'] = owner
        context['description'] = description
        context['tags'] = tags
        context['borrower'] = borrower
        context['condition'] = condition
        context['available'] = available
        context['ownedByUser'] = ownedByUser
        context['meetsMin'] = meetsMinRep
        context.update(content.genBaseLoggedIn(request))
        if contextArg:
            context.update(contextArg)
        return render_to_response('tool_page.html', context)
     
def view_shed_page(request, id, contextArg):#contextArg is a dict to be added to the content dict
    if request.user.is_anonymous():
        return HttpResponseRedirect("/accounts/login")
    else:
        if id is not None:
            try:
                shedObj = shedUtil.getShedFromID(id)
            except ObjectDoesNotExist:
                context = {}
                context['object'] = 'shed'
                context.update(content.genBaseLoggedIn(request))
                return render_to_response("dne.html", context)
        else:
            context = {}
            context['object'] = 'shed'
            context.update(content.genBaseLoggedIn(request))
            return render_to_response("dne.html", context)
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
        context['shed'] = shedObj
        context['owner'] = owner
        context['name'] = name
        context['admins'] = admins
        context['members'] = members
        context['tools'] = tools
        context['meetsMin'] = meetsMinRep
        context['alreadyMember'] = shedMembership
        context.update(content.genBaseLoggedIn(request))
        if contextArg:
            context.update(contextArg)
        return render_to_response('shed_page.html', context)

def view_community_page(request, sharezone):
    if request.user.is_anonymous():
        return HttpResponseRedirect("/accounts/login")
    else:
        if sharezone is not None:
            sheds = shedUtil.getAllShedsInSharezone(sharezone)
            users = profileUtil.getAllProfilesInSharezone(sharezone)
            context = {}
            context['sharezone'] = sharezone
            context['sheds'] = sheds
            context['users'] = users
            context.update(content.genBaseLoggedIn(request))
            return render_to_response('community_page.html', context)
        else:
            context = {}
            context['object'] = 'community'
            context.update(content.genBaseLoggedIn(request))
            return render_to_response('dne.html', context)

#a view that will display all tools
def all_tools(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        tools = toolUtil.getAllTools()
        context = {}
        context.update(csrf(request))
        context['tools'] = tools
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('all_tools.html', context)

def borrow_tool(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        borrowerProfile = profileUtil.getProfileFromUser(request.user)
        toolObject = toolUtil.getToolFromID(id)
        ownerProfile = toolObject.owner
        actionObject = actionUtil.createBorrowRequestAction(toolObject, borrowerProfile)
        return HttpResponseRedirect('/tools/' + id + '/request_sent')

def join_shed(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        joinerProfile = profileUtil.getProfileFromUser(request.user)
        shedObject = shedUtil.getShedFromID(id)
        ownerProfile = shedObject.owner
        actionObject = actionUtil.createShedRequestAction(shedObject, joinerProfile)
        return HttpResponseRedirect('/sheds/' + id + '/request_sent')

def request_sent(request):
    return render_to_response("request_sent.html", content.genBaseLoggedIn(request))

def request_accept(request, id):
    notifObject = Notification.objects.get(id = id)
    notifObject = notifUtil.respondToNotif(notifObj, "Accept")
    actionObject = notifUtil.getNotifSourceObject(notifObject)
    requesterProfile = actionObject.requester
    context = {}
    context['requesterName'] = requesterProfile.user.username
    if actionUtil.isShedRequest(actionObject):
        shedObject = actionObject.shed
        shedName = shedObject.name
        context['objectName'] = shedName
        context['type'] = "Shed"
    elif actionUtil.isToolRequest(actionObject):
        toolObject = actionObject.tool
        toolName = toolObject.name
        context['objectName'] = shedName
        context['type'] = "Tool"
    context.update(content.genBaseLoggedIn(request))
    return render_to_response("request_accept.html", context)

def request_decline(request, id):
    notifObject = Notification.objects.get(id = id)
    notifObject = notifUtil.respondToNotif(notifObj, "Deny")
    actionObject = notifUtil.getNotifSourceObject(notifObject)
    requesterProfile = actionObject.requester
    context = {}
    context['requesterName'] = requesterProfile.user.username
    if actionUtil.isShedRequest(actionObject):
        shedObject = actionObject.shed
        shedName = shedObject.name
        context['objectName'] = shedName
        context['type'] = "Shed"
    elif actionUtil.isToolRequest(actionObject):
        toolObject = actionObject.tool
        toolName = toolObject.name
        context['objectName'] = shedName
        context['type'] = "Tool"
    context.update(content.genBaseLoggedIn(request))
    return render_to_response("request_deny.html", context)

def view_notifications(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        return render_to_response('view_notifs.html', content.genViewNotifications(request))

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
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('all_sheds.html', context)

def about_us(request):
    return render_to_response('about_us.html', content.genSuper())

#DO NOT TOUCH - team leader (<-- lol)
def spooked(request):
    return render_to_response('spoopy.html')

def dne(request):
    context.update(content.genBaseLoggedIn(request))
    return render_to_response("dne.html", context)

def spooky(request):
    return render_to_response('spagett.html')