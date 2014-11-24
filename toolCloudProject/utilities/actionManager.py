"""
What calls action manager:
    when .save() is called on an action object
    when .save() is called on a notification object
What action manager does:
    Updates every single Action object in the database
    depending on what state each object is currently in.
    Basically contains the all of the logic behind tool borrowing
    and shed requests.

ADAM (Code Fairy) LOOK HERE!!

    When a person clicks the button on the UI to request a tool, the UI should
    call a method in actionUtilities called createBorrowRequestAction(tool, requester).
    This will create an action object with a currentState equal to "userBorrowRequest"
    which will ultimately result in sending a request notification to the owner of the tool.
    
    We must update the UI so that two buttons display with "Accept" or "Deny" for
    all tool request notifications. The UI will do this for all notifications that
    evaluate to true after calling the isRequestNotif() notification utility on them.
    Clicking the accept button will call acceptBorrowRequest(), deny calls denyBorrowRequest()
    Both of those functions are apart of notificationUtilities and will change the action
    object's currentState field to "borrowed" or "idle" respectively.

    We must update the UI so that when the "Return Tool" button is clicked,
    it calls a tool utility called returnTool(toolObject) which changes the
    action object's currentState field to "returned". This'll ultimately create a new
    info notif telling the owner that the tool has been returned.

    #### ADDITIONAL SHED JOINING UI IMPLEMENTATIONS #####

    When the "Join Shed" button is clicked on the UI, the UI should call a actionUtilities
    method createShedRequestAction(shed,requester). That should be all that button needs to do.

    No other shed joining UI stuff is needed. Everything else from that point on is handled
    by the state machine.
"""

import utilities.profileUtilities as profileUtil
import utilities.shedUtilities as shedUtil
import utilities.toolUtilities as toolUtil
import utilities.notificationUtilities
import utilities.actionUtilities as actionUtil
import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.utils import timezone

"""
    Update every Action object in the database depending
    on what state each action is currently in.
"""
def processActions():
    #Re-process all action objects in the database
    for actionInstance in actionUtil.getAllActions():
        #states allow system to process and respond to all actions asynchronously
        #Tool borrow state machine
        if actionUtil.isToolRequest(actionInstance):

            if actionInstance.currrentState == "userBorrowRequest":  #entry point
                #proceed to next state where the owner is asked if this user can borrow his tool
                actionInstance.currrentState = "askOwner"
                actionInstance.save()
                processActions()

            if actionInstance.currrentState == "askOwner":
                #proceed to next state
                actionInstance.currrentState = "acceptDecline"
                actionInstance.save()
                #send a request notification to the user who's tool is being requested
                #the response options will be "Accept" or "Deny"
                question = "Can " + actionInstance.requester.user.username + " borrow your " + \
                                actionInstance.tool.name + " from " + actionInstance.tool.myShed.name + "?"
                userOptions = "Accept,Deny" #adding options       
                utilities.notificationUtilities.createResponseNotif(actionInstance, actionInstance.tool.owner, \
                                                            question, options = userOptions)
                processActions()

            elif actionInstance.currrentState == "acceptDecline":
                #if the owner of the tool has responded to the tool request notification:
                if utilities.notificationUtilities.notifHasResponse(actionUtil.getNotifOfAction(actionInstance)):
                   # if the owner of the tool accepted the tool request:
                    if utilities.notificationUtilities.getNotifResponse(actionUtil.getNotifOfAction(actionInstance)) == 'Accept':
                        #update the tool's borrowedTime field
                        actionInstance.tool.borrowedTime = timezone.now()
                        #update tool's borrower field
                        toolUtil.updateToolBorrower(actionInstance.tool,actionInstance.requester)
                        #move tool location to requester's shed
                        targetShed = shedUtil.getShedByName(profileUtil.getUserOfProfile(actionInstance.requester).username + "'s Shed")[0]
                        #save the name of the shed that the tool used to be in
                        actionInstance.workSpace = actionInstance.tool.myShed.name
                        #remove the tool from it's old location first
                        shedUtil.removeToolFromShed(actionInstance.tool.myShed, actionInstance.tool)
                        #then add the tool to the requester's personal shed
                        shedUtil.addToolToShed(targetShed, actionInstance.tool)
                        #delete the borrow request notification from the database so it no longer displays
                        actionUtil.getNotifOfAction(actionInstance).delete()
                        #proceed to next state
                        actionInstance.currrentState = "borrowed"
                        actionInstance.save()

                    # the owner of the tool declined the borrowing of the tool
                    else:
                        #send an info notification to the requester saying he was denied
                        response = "You have been denied from borrowing " + \
                                        actionInstance.tool.name + " from " + actionInstance.tool.myShed.name
                        utilities.notificationUtilities.createInfoNotif(actionInstance,actionInstance.requester,response)
                        #proceed to next state
                        actionInstance.currrentState = "idle"
                        actionInstance.save()

            elif actionInstance.currrentState == "borrowed":
                #check if borrowedTime of tool was older than [maxBorrowTime] days ago
                if toolUtil.toolIsOverdraft(actionInstance.tool):
                    #notify requester that they are overdraft and they should return [tool]
                    message = "Uh oh...your " + actionInstance.tool.name + " is overdraft!"
                    utilities.notificationUtilities.createInfoNotif(actionInstance, actionInstance.requester, message)
                    #move to overdraft state
                    actionInstance.currentState = "overdraft"
                    actionInstance.save()
                processActions()

            elif actionInstance.currrentState == "overdraft":
                #disable the user from borrowing any more tools
                actionInstance.tool.borrower.canBorrow = False
                actionInstance.save()
                processActions()

            #moving into the "returned" state is handled by the UI
            elif actionInstance.currrentState == "returned":
                #notify tool owner that his tool has been returned
                message = "Your " + actionInstance.tool.name + " has been returned to " + \
                                actionInstance.tool.myShed.name
                utilities.notificationUtilities.createInfoNotif(actionInstance, actionInstance.tool.owner, message)
                #reduce user reputation by 5 for every day the tool is late!
                timeSinceBorrowed = timezone.now() - toolObj.borrowedTime
                for day in range(timeSinceBorrowed.days):
                    actionInstance.tool.borrower.reputation -= 5
                #update the tool's borrower field
                actionInstance.tool.borrower = None
                #remove the tool from personal shed and move it back to the shed it was borrowed from
                shedUtil.removeToolFromShed(actionInstance.tool.myShed, actionInstance.tool)
                oldShed = toolUtil.getShedByName(actionInstance.workSpace)
                shedUtil.addToolToShed(oldShed, actionInstance.tool)
                #move to idle state
                actionInstance.currentState = "idle"
                actionInstance.save()
                processActions()

            elif actionInstance.currrentState == "idle":
                #delete action object
                actionInstance.delete()
                processActions()

    
        elif actionUtil.isShedRequest(actionInstance):

            #this state will be entered when the "Join Shed" button is clicked
            if actionInstance.currentState == "userShedRequest":
                #send shed request notif to all admins of shed and the shed owner
                adminList = shedUtil.getAllAdminsOfShed(actionInstance.shed)
                for admin in adminList:
                    actionUtil.createShedRequestAction(actionInstance.shed,actionInstance.requester)
                #also send a shed request notif to the owner of the shed
                actionUtil.createShedRequestAction(actionInstance.shed,actionInstance.shed.owner)
                #move to acceptDeny state
                actionInstance.currentState = "acceptDeny"
                actionInstance.save()
                processActions()

            elif actionInstance.currentState == "acceptDeny":
                #if the notification has been responded to
                if utilities.notificationUtilities.notifHasResponse(getNotifOfAction(actionInstance)):
                    #if the admin responded 'Accept'
                    if utilities.notificationUtilities.getNotifResponse(getNotifOfAction(actionInstance)) == 'Accept':
                        #add the guy to the shed
                        shedUtil.addMemberToShed(actionInstance.shed, actionInstance.requester)
                        #delete the notif that asked about accepting and denying
                        actionUtil.getNotifOfAction(actionInstance).delete()
                        actionInstance.currentState = "idle"
                        actionInstance.save()
                    else:
                        #send an info notification to the requester saying he was denied
                        message = "You have been denied from joining " + actionInstance.shed.name
                        utilities.notificationUtilities.createInfoNotif(actionInstance,actionInstance.requester,message)
                        #proceed to next state
                        actionInstance.currrentState = "idle"
                        actionInstance.save()
                processActions()

            elif actionInstance.currentState == "idle":
                print("help im dying")
                #delete the action object from the database
                actionInstance.delete()
                processActions()
