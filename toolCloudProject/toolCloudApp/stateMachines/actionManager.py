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
                #send a response notification to the user who's tool is being requested
                #the response options will be "Accept" or "Decline"
                
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
                #if the owner of the tool has responded to the tool request notification
                if notifHasResponse(getNotifOfAction(actionInstance)) == True:
                   
                    if notifUtil.getNotifResponse(getNotifOfAction(actionInstance)) == 'Accept':
                        #start timer for when tool is overdue (set end time)
                        #move tool location to requester's shed

                        #target shed is the requester's personal shed
                        targetShed = shedUtil.getShedByName(profileUtil.getUserOfProfile(actionInstance.requester).username + "'s Shed")
                        #remove the tool from it's old location first
                        shedUtil.removeToolFromShed(actionInstance.tool.shed,actionInstance.tool)
                        #then add the tool to the requester's personal shed
                        shedUtil.addToolToShed(targetShed,actionInstance.tool)
                        #update tool's borrower field
                        toolUtil.updateToolBorrower(actionInstance.tool,getUserOfProfile(actionInstance.requester))

                        #proceed to next state
                        actionInstance.currrentState = "borrowed"
                        actionInstance.save()
                        actionUtil.getNotifOfAction(actionInstance).delete()
                        #ProcessActions()       #re-invoke entire state machine

                    else: # the owner of the tool declined the borrowing of the tool

                        #send an info notification to the requester saying he was denied
                        response = "You have been swiftly rejected from borrowing " + \
                                        actionInstance.tool.name + " from " + actionInstance.tool.shed

                        notifUtil.createInfoNotif(actionInstance,actionInstance.requester,response):

                        #proceed to next state
                        actionInstance.currrentState = "idle"
                        actionInstance.save()
                        #ProcessActions()       #re-invoke entire state machine

            elif actionInstance.currrentState == "borrowed":
                #check if borrowed is past timestamp
                    #Notify {requester} that they are overdraft and they should return [tool]
                    #Set canBorrow state to false
                    #move to overdraft state

                #if (tool.isAvailable() == true):   #means tool has been returned
                    #move state to returned 

                #proceed to next state
                #actionInstance.currrentState = "borrowed"
                #actionInstance.save()
                #ProcessActions()       #re-invoke entire state machine


            elif actionInstance.currrentState == "overDraft":
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

            elif actionInstance.currrentState == "idle":        #this state does nothing and will get deleted after a while
                #delete action object
                pass



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
