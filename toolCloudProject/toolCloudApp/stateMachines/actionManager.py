"""
What calls action manager:
    automated
    update to one of the action objects
    call back from a notification object

    For reference:

    class Action(models.Model):
        tool = models.ForeignKey('Tool', related_name='toolActions',null = True) #if tool, send to owner of tool
        shed = models.ForeignKey('Shed', related_name='shedActions',null = True) #if shed, send to all admins of shed
        requester = models.ForeignKey('Profile', related_name='requesterActions')

        actionType = models.CharField(max_length=20)#either tool, or shed
        currrentState = models.CharField(max_length=20)
        timeStamps = models.CharField(max_length=560,default = "") #CSV timestamps for every state
        workSpace = models.CharField(max_length=200,null = True) #for use in state machine
"""

import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed, Notification, Action
import utilities.profileUtilities as profileUtil
import utilities.shedUtilities as shedUtil
import utilities.toolUtilities as toolUtil
import utilities.notificationUtilities as notifUtil
import utilities.actionUtilities as actionUtil

def ProcessActions():
    #Re-process all action objects on every call
    for actionInstance in getAllActions():
        #states allow system to process and respond to all actions asynchronously
        #Tool borrow state machine
        if isToolRequest() == True:

            if actionInstance.currrentState == "userBorrowRequest":  #entry point
                #proceed to next state where the owner is asked if this user can borrow his tool
                actionInstance.currrentState = "askOwner"
                actionInstance.save()
                #ProcessActions()   #re-invoke entire state machine

            if actionInstance.currrentState == "askOwner":
                #send a request notification to the user who's tool is being requested
                #the response options will be "Accept" or "Deny"
                """ ADAM LOOK HERE!! """
                #we must update the UI so that two buttons display with "Accept" or "Deny"
                #the UI will do this for all notifications that eval to true on the isRequestNotif() utility
                #clicking accept button will call acceptBorrowRequest(), deny calls denyBorrowRequest()
                #both of those functions are apart of notificationUtilities
                question = "Can " + actionInstance.requester.name + " borrow your " + \
                                actionInstance.tool.name + " from " + actionInstance.tool.shed + "?"
                userOptions = "Accept,Deny" #adding options       
                notifUtil.createResponseNotif(actionInstance, actionInstance.tool.owner, \
                                                            question, options = userOptions)
                #proceed to next state
                actionInstance.currrentState = "acceptDecline"
                actionInstance.save()
                #ProcessActions()       #re-invoke entire state machine

            elif actionInstance.currrentState == "acceptDecline":
                #if the owner of the tool has responded to the tool request notification:
                if notifHasResponse(getNotifOfAction(actionInstance)):
                   # if the owner of the tool accepted the tool request:
                    if notifUtil.getNotifResponse(getNotifOfAction(actionInstance)) == 'Accept':
                        #update the tool's borrowedTime field
                        actionInstance.tool.borrowedTime = timezone.now()
                        #update tool's borrower field
                        toolUtil.updateToolBorrower(actionInstance.tool,getUserOfProfile(actionInstance.requester))
                        #move tool location to requester's shed
                        targetShed = shedUtil.getShedByName(profileUtil.getUserOfProfile(actionInstance.requester).username + "'s Shed")
                        #remove the tool from it's old location first
                        shedUtil.removeToolFromShed(actionInstance.tool.shed, actionInstance.tool)
                        #then add the tool to the requester's personal shed
                        shedUtil.addToolToShed(targetShed, actionInstance.tool)
                        #delete the borrow request notification from the database so it no longer displays
                        actionUtil.getNotifOfAction(actionInstance).delete()
                        #proceed to next state
                        actionInstance.currrentState = "borrowed"
                        actionInstance.save()
                        #ProcessActions()       #re-invoke entire state machine

                    # the owner of the tool declined the borrowing of the tool
                    else:
                        #send an info notification to the requester saying he was denied
                        response = "You have been denied from borrowing " + \
                                        actionInstance.tool.name + " from " + actionInstance.tool.shed
                        notifUtil.createInfoNotif(actionInstance,actionInstance.requester,response)
                        #proceed to next state
                        actionInstance.currrentState = "idle"
                        actionInstance.save()
                        #ProcessActions()       #re-invoke entire state machine

            elif actionInstance.currrentState == "borrowed":
                #check if borrowed is past timestamp
                #need to update tool model with a new field toolBorrowed
                #need to update tool utils with toolIsOverdraft()
                if toolUtil.toolIsOverdraft(actionInstance.tool):
                    #notify requester that they are overdraft and they should return [tool]
                    message = "Uh oh...your " + actionInstance.tool.name + " is overdraft!"
                    notifUtil.createInfoNotif(actionInstance, actionInstance.requester, message)
                    #set canBorrow state to false
                    actionInstance.requester.canBorrow = False
                    #move to overdraft state
                    actionInstance.currentState = "overdraft"
                    actionInstance.save()

                # if the tool has already been returned
                if (actionInstance.tool.isAvailable() == True):
                    actionInstance.currentState = "returned"
                    actionInstance.save()

                #ProcessActions()       #re-invoke entire state machine


            elif actionInstance.currrentState == "overdraft":
                #if (tool.isAvailable() == true):   #means tool has been returned
                    #calculate how many days the tool is overdue and reduce user reputation until then
                    #set user.canBorrow state to true.
                    #notify requester thankyou for returning the tool finally!
                    #move state to returned 

                pass
            elif actionInstance.currrentState == "returned":
                #Notify tool owner that his tool has been returned
                #move to idle state
                pass
            
            elif actionInstance.currrentState == "idle":
                #delete action object
                actionInstance.delete()



        # #shed request state machine

        # if isShedRequest() == True:
        #     if state == "userShedRequest":
        #         #proceed to next state
        #         pass
        #     elif state == "askAdmins":
        #         #loop through all admins of shed
        #             #generate question string asking [Admin] if [borrower]

        #             #proced to next state
        #         pass

        #     elif state == "acceptDecline":
        #         #get all notificaitons assosiated with this action
        #             #check if notification has been responded to correctly

        #         pass
