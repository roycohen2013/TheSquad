from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
import django.db
from toolCloudApp.models import Profile, Tool, Shed, User, Notification, Action
from toolCloudApp.mailSend import sendMail
from toolCloudApp.search import *
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
import utilities.actionManager as actionManager
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
from toolCloudApp.forms import UserRegistrationForm, ToolCreationForm, ShedCreationForm, passwordResetForm, UserEditForm, ToolEditForm, ShedEditForm


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
                sendMail(profileUtil.getProfileFromUser(userAccount), \
                    "Welcome aboard! ", "Thank you for registering with ToolCloud.")
                shedName = form.cleaned_data['username'] + "'s Shed"
                userProfile = profileUtil.getProfileFromUser(userAccount)
                newShedObject = Shed(name=shedName, owner=userProfile, location='location', sharezone=form.cleaned_data['zip_code'],\
                    status='status')
                newShedObject.save()
                newShedObject.members.add(userProfile)
                newShedObject.admins.add(userProfile)
                newShedObject.save()
                userProfile.personalShed = newShedObject
                context = {}
                context.update(content.genUserHome(request))
                context.update(content.addGoodRegisterNoti(dict()))
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

def edit_user_info(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login/')
    else:
        if request.method == 'POST':
            profileObj = profileUtil.getProfileFromUser(request.user)
            form = UserEditForm(profileObj, request.POST)
            if form.is_valid():
                profileObj = form.save()
                return HttpResponseRedirect('/accounts/my_account/account_updated')
        else:
            form = UserEditForm(profileUtil.getProfileFromUser(request.user))
        context = {}
        context.update(csrf(request))
        context.update(content.genBaseLoggedIn(request))
        context['form'] = form
        return render_to_response('user_update.html', context)

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
                sendMail(profileUtil.getProfileFromUser(request.user), \
                    "Your tool has been submitted! ",\
                     "Thanks for submitting your " + tool.name + \
                      " to ToolCloud.  We'll let you know when someone wants to borrow it.")
                return HttpResponseRedirect('/tools/' + str(tool.id) + '/success')
        else:
            form = ToolCreationForm(request.user)
        context = {}
        context.update(csrf(request))
        context.update(content.genBaseLoggedIn(request))
        context['form'] = form
        return render_to_response('tool_creation.html', context)

def edit_tool(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login/')
    else:
        if request.method == 'POST':
            toolObj = toolUtil.getToolFromID(id)
            form = ToolEditForm(toolObj, request.POST)
            if form.is_valid():
                toolObj = form.save()
                return HttpResponseRedirect('/tools/' + str(toolObj.id) + '/edit/success')
        else:
            toolObj = toolUtil.getToolFromID(id)
            form = ToolEditForm(toolObj)
        context = {}
        context.update(csrf(request))
        context.update(content.genBaseLoggedIn(request))
        context['form'] = form
        context['tool'] = toolUtil.getToolFromID(id)
        return render_to_response('tool_update.html', context)

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
                profileObj = profileUtil.getProfileFromUser(request.user)
                shed.members.add(profileObj)
                shed.admins.add(profileObj)
                #send email
                sendMail(profileUtil.getProfileFromUser(request.user), \
                    "Your shed has been created! ", \
                    "Thanks for creating " + shed.name + \
                    " on ToolCloud.  We'll let you know when someone wants to join.")
                return HttpResponseRedirect('/sheds/' + str(shed.id) + '/success')
        else:
            form = ShedCreationForm(request.user)
        context = {}
        context.update(csrf(request))
        context['form'] = form
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('shed_creation.html', context)

def edit_shed(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login/')
    else:
        if request.method == 'POST':
            shedObj = shedUtil.getShedFromID(id)
            form = ShedEditForm(shedObj, request.POST)
            if form.is_valid():
                shedObj = form.save()
                return HttpResponseRedirect('/sheds/' + str(shedObj.id) + '/edit/success')
        else:
            form = ShedEditForm(shedUtil.getShedFromID(id))
        context = {}
        context.update(csrf(request))
        context.update(content.genBaseLoggedIn(request))
        context['form'] = form
        context['shed'] = shedUtil.getShedFromID(id)
        return render_to_response('shed_update.html', context)

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

def view_current_profile(request, contextArg):
    """this view displays account information and allows users to edit their information
    """
    if request.user.is_anonymous():
        #tell user they need to be logged in to do that
        return HttpResponseRedirect('/accounts/login/') #redirect to login page
    else:
        currentUser = request.user
        userProfile = profileUtil.getProfileFromUser(currentUser)
        print(userProfile.personalShed)
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
        if contextArg:
            context.update(contextArg)
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
            context = {}
            context['object'] = 'tool'
            context.update(content.genBaseLoggedIn(request))
            return render_to_response("dne.html", context)
        owner = toolUtil.getToolOwner(toolObj)
        name = toolUtil.getToolName(toolObj)
        description = toolUtil.getToolDescription(toolObj)
        tags = toolUtil.getToolTags(toolObj)
        borrower = toolUtil.getToolBorrower(toolObj)
        condition = toolUtil.getToolConditionReadable(toolObj)
        available = toolUtil.isToolAvailable(toolObj)
        actions = actionUtil.getProfileAction(profileUtil.getProfileFromUser(request.user))
        actionBorrowRequest = None
        actionReturnRequest = None
        requesterProfile = None
        for action in actions:
            if action.tool == toolObj:
                if action.currrentState == "userBorrowRequest" or action.currrentState == "acceptDecline":
                    actionBorrowRequest = action
                if action.currrentState == "markedReturned" or action.currrentState == "confirmReturned":
                    actionReturnRequest = action
        if actionBorrowRequest:
            pendingBorrowRequest = True
            requesterProfile = actionBorrowRequest.requester
        else:
            pendingBorrowRequest = False
        if actionReturnRequest:
            pendingReturnRequest = True
        else:
            pendingReturnRequest = False
        if profileUtil.getProfileFromUser(request.user) == owner:
            ownedByUser = True
        else:
            ownedByUser = False
        meetsMinRep = (profileUtil.getReputation(profileUtil.getProfileFromUser(request.user)) >= toolObj.minimumReputation)
        profileObj = (profileUtil.getProfileFromUser(request.user))
        canBorrow = profileObj.canBorrow
        context = {}
        context.update(csrf(request))
        context['tool'] = toolObj
        context['name'] = name #TODO change to toolName
        context['owner'] = owner
        context['description'] = description
        context['tags'] = tags
        context['currentProfile'] = profileObj
        context['borrower'] = borrower
        context['requester'] = requesterProfile
        context['condition'] = condition
        context['available'] = available
        context['ownedByUser'] = ownedByUser
        context['meetsMin'] = meetsMinRep
        context['pendingBorrowRequest'] = pendingBorrowRequest
        context['pendingReturnRequest'] = pendingReturnRequest
        context['canBorrow'] = canBorrow
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
        isAdmin = False
        for admin in admins:
            if admin == profileUtil.getProfileFromUser(request.user):
                isAdmin = True
        members = shedUtil.getAllMembersOfShed(shedObj)
        tools = toolUtil.getAllToolsInShed(shedObj)
        userProfile = profileUtil.getProfileFromUser(request.user)
        meetsMinRep = userProfile.reputation >= shedObj.minimumReputation
        shedMembership = shedUtil.checkForMembership(userProfile, id)
        actions = actionUtil.getProfileAction(profileUtil.getProfileFromUser(request.user))
        actionRequest = None
        pendingRequest = False
        for action in actions:
            if action.shed == shedObj:
                actionRequest = action
        if actionRequest:
            if actionRequest.currrentState == "userShedRequest" or actionRequest.currrentState == "acceptDeny":
                pendingRequest = True
        context = {}
        context.update(csrf(request))
        context['shed'] = shedObj
        context['owner'] = owner
        context['currentUser'] = profileUtil.getProfileFromUser(request.user)
        context['name'] = name
        context['admins'] = admins
        context['members'] = members
        context['tools'] = tools
        context['meetsMin'] = meetsMinRep
        context['alreadyMember'] = shedMembership
        context['isAdmin'] = isAdmin
        context['pendingRequest'] = pendingRequest
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

def return_tool(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        toolObj = toolUtil.getToolFromID(id)
        actionObj = actionUtil.getBorrowedToolAction(toolObj)
        actionObj.currrentState = "markedReturned"
        actionObj.save()
        actionManager.processActions()
        return HttpResponseRedirect('/tools/' + id + '/returned')

def join_shed(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        joinerProfile = profileUtil.getProfileFromUser(request.user)
        shedObject = shedUtil.getShedFromID(id)
        ownerProfile = shedObject.owner
        actionObject = actionUtil.createShedRequestAction(shedObject, joinerProfile)
        actionManager.processActions()
        return HttpResponseRedirect('/sheds/' + id + '/request_sent')

def request_accept(request, id):
    notifObject = Notification.objects.get(id = id)
    notifObject = notifUtil.respondToNotif(notifObject, "Accept")
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
        context['objectName'] = toolName
        context['type'] = "Tool"
    context.update(content.genBaseLoggedIn(request))
    actionUtil.forceProcessActions()
    return render_to_response("view_notifs.html", content.addRequestApprovedNoti(context))

def request_decline(request, id):
    notifObject = Notification.objects.get(id = id)
    notifObject = notifUtil.respondToNotif(notifObject, "Deny")
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
        context['objectName'] = toolName
        context['type'] = "Tool"
    context.update(content.genBaseLoggedIn(request))
    actionUtil.forceProcessActions()
    return render_to_response("view_notifs.html", content.addRequestDeniedNoti(context))

def confirm_add_shed_admin(request, id, username):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        newAdmin = profileUtil.getProfileFromUser(User.objects.get(username=username))
        admins = shedUtil.getAllAdminsOfShed(shedObj)
        isAdmin = False
        for admin in admins:
            if admin == userProfile:
                isAdmin = True
        if isAdmin:
            context = {}
            context['currentUser'] = userProfile
            context['shed'] = shedObj
            context['newAdmin'] = newAdmin
            context.update(content.genBaseLoggedIn(request))
            return render_to_response("admin_confirm.html", context)
        else:
            return HttpResponseRedirect('/')

def add_shed_admin(request, id, username):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        newAdmin = profileUtil.getProfileFromUser(User.objects.get(username=username))
        admins = shedUtil.getAllAdminsOfShed(shedObj)
        isAdmin = False
        for admin in admins:
            if admin == userProfile:
                isAdmin = True
        if isAdmin:
            shedObj.admins.add(newAdmin)
            notifUtil.createInfoNotif(shedObj, newAdmin, "You have been made an admin of the shed " + shedObj.name + "! ")
            return HttpResponseRedirect("/sheds/" + str(shedObj.id) + "/add_admin/added/success")
        else:
            return HttpResponseRedirect('/')

def confirm_remove_shed_admin(request, id, username):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        removeAdmin = profileUtil.getProfileFromUser(User.objects.get(username=username))
        if shedObj.owner == removeAdmin:
            return HttpResponseRedirect('/')
        else:
            if shedObj.owner == userProfile:
                context = {}
                context['currentUser'] = userProfile
                context['shed'] = shedObj
                context['removeAdmin'] = removeAdmin
                context.update(content.genBaseLoggedIn(request))
                return render_to_response("admin_remove_confirm.html", context)
            else:
                return HttpResponseRedirect('/')

def remove_shed_admin(request, id, username):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        removeAdmin = profileUtil.getProfileFromUser(User.objects.get(username=username))
        if shedObj.owner == removeAdmin:
            return HttpResponseRedirect('/')
        else:
            if shedObj.owner == userProfile:
                shedUtil.removeAdminFromShed(shedObj, removeAdmin)
                notifUtil.createBadInfoNotif(shedObj, removeAdmin, "You have been removed as an admin from the shed " + shedObj.name + ". ")
                return HttpResponseRedirect('/sheds/' + str(shedObj.id) + '/remove_admin/removed/success')
            else:
                return HttpResponseRedirect('/')

def confirm_remove_shed_member(request, id, username):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        banUser = profileUtil.getProfileFromUser(User.objects.get(username=username))
        admins = shedUtil.getAllAdminsOfShed(shedObj)
        isAdmin = False
        for admin in admins:
            if admin == userProfile:
                isAdmin = True
        if isAdmin:
            context = {}
            context['currentUser'] = userProfile
            context['shed'] = shedObj
            context['banned'] = banUser
            context.update(content.genBaseLoggedIn(request))
            return render_to_response("remove_member_confirm.html", context)
        else:
            return HttpResponseRedirect('/')

def remove_shed_member(request, id, username):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        banUser = profileUtil.getProfileFromUser(User.objects.get(username=username))
        admins = shedUtil.getAllAdminsOfShed(shedObj)
        userIsAdmin = False
        banUserIsAdmin = False
        for admin in admins:
            if admin == userProfile:
                userIsAdmin = True
            elif admin == banUser:
                banUserIsAdmin = True
        if userIsAdmin:
            if banUserIsAdmin:
                if shedObj.owner == userProfile:
                    shedUtil.removeAdminFromShed(shedObj, banUser)
                    notifUtil.createBadInfoNotif(shedObj, banUser, "You have been removed as an admin from the shed " + shedObj.name + ". ")
                    shedUtil.removeMemberFromShed(shedObj, banUser)
                    notifUtil.createBadInfoNotif(shedObj, banUser, "You have been kicked from the shed " + shedObj.name + ". ")
                    shedTools = toolUtil.getAllToolsInShed(shedObj)
                    for tool in shedTools:
                        if tool.owner == banUser:
                            shedUtil.removeToolFromShed(shedObj, tool)
                            shedUtil.addToolToShed(banUser.personalShed, tool)
                    return HttpResponseRedirect("/sheds/" + str(shedObj.id) + "/remove_member/kicked/success")
                else:
                    return HttpResponseRedirect('/')
            else:
                shedUtil.removeMemberFromShed(shedObj, banUser)
                shedObj.bannedUsers.add(banUser)
                notifUtil.createBadInfoNotif(shedObj, banUser, "You have been kicked from the shed " + shedObj.name + ". ")
                shedTools = toolUtil.getAllToolsInShed(shedObj)
                for tool in shedTools:
                    if tool.owner == banUser:
                        shedUtil.removeToolFromShed(shedObj, tool)
                        shedUtil.addToolToShed(banUser.personalShed, tool)
                return HttpResponseRedirect("/sheds/" + str(shedObj.id) + "/remove_member/kicked/success")
        else:
            return HttpResponseRedirect('/')

def confirm_leave_shed(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        context = {}
        context['currentUser'] = userProfile
        context['shed'] = shedObj
        return render_to_response("leave_shed_confirm.html", context)

def leave_shed(request, id):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        userProfile = profileUtil.getProfileFromUser(request.user)
        shedObj = shedUtil.getShedFromID(id)
        if shedObj.owner == userProfile:
            return HttpResponseRedirect('/')
        else:
            admins = shedUtil.getAllAdminsOfShed(shedObj)
            for admin in admins:
                if admin == userProfile:
                    shedUtil.removeAdminFromShed(shedObj, userProfile)
            shedUtil.removeMemberFromShed(shedObj, userProfile)
            shedTools = toolUtil.getAllToolsInShed(shedObj)
            for tool in shedTools:
                if tool.owner == userProfile:
                    shedUtil.removeToolFromShed(shedObj, tool)
                    shedUtil.addToolToShed(userProfile.personalShed, tool)
            return HttpResponseRedirect('/sheds/' + str(shedObj.id) + '/leave/success')

def view_notifications(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        return render_to_response('view_notifs.html', content.genBaseLoggedIn(request))

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
    
def password_reset(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = passwordResetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            passone = form.cleaned_data.get ("password")
            passtoo = form.cleaned_data.get ("confirm_password")
            if (passone == passtoo):
                request.user.set_password (passone)
                request.user.save()
                sendMail(profileUtil.getProfileFromUser(request.user), \
                    "Your password has been changed", \
                    "Your password has been changed on ToolCloud.")
            return HttpResponseRedirect('/accounts/my_account/password_changed')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = passwordResetForm()

    return render(request, 'password_reset.html', {'form': form})

def search(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/accounts/login')
    else:
        query_string = ''
        found_entries = None
        no_results = True
        tool_results = []
        profile_results =[]
        shed_results = []
        if ('q' in request.GET) and request.GET['q'].strip():
            query_string = request.GET['q']
            if query_string == '' or query_string == None:
                tool_results = None
                profile_results = None
                shed_results = None
            else:
                entry_query = get_query(query_string, ['name'])
                found_tools = Tool.objects.filter(name__icontains=query_string)
                tool_results = list(found_tools)
                found_tools = Tool.objects.filter(tags__icontains=query_string)
                for tool in found_tools:
                    if tool not in tool_results:
                        tool_results.append(tool)
                found_tools = Tool.objects.filter(description__icontains=query_string)
                for tool in found_tools:
                    if tool not in tool_results:
                        tool_results.append(tool)
                found_profiles = Profile.objects.filter(user__username__icontains=query_string)
                profile_results = list(found_profiles)
                found_profiles = Profile.objects.filter(user__first_name__icontains=query_string)
                for profile in found_profiles:
                    if profile not in profile_results:
                        profile_results.append(profile)
                found_profiles = Profile.objects.filter(user__last_name__icontains=query_string) 
                for profile in found_profiles:
                    if profile not in profile_results:
                        profile_results.append(profile)
                found_sheds = Shed.objects.filter(name__icontains=query_string)
                shed_results = list(found_sheds)
                all_results = shed_results + profile_results + tool_results
                no_results = False
                if all_results == []:
                    no_results = True
        context = {}
        context.update(csrf(request))
        context['p_results'] = profile_results
        context['t_results'] = tool_results
        context['s_results'] = shed_results
        context['no_results'] = no_results
        context.update(content.genBaseLoggedIn(request))
        return render_to_response('search.html', context)
        