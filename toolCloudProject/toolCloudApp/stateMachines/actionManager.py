
import sys
sys.path.append("..")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed, Notification, Action



#what calls action manager:
    #Automated
    #update to one of the action objects
    #call back from a notification object


#reference
    """
    class Action(models.Model):
        tool = models.ForeignKey('Tool', related_name='toolActions')#if tool, send to owner of tool
        shed = models.ForeignKey('Shed', related_name='shedActions')#if shed, send to all admins of shed
        admin = models.ForeignKey('Profile', related_name='adminActions')#returns list of actions that a user is controlling of
        requester = models.ForeignKey('Profile', related_name='requesterActions')

        actionType = models.CharField(max_length=20)#either tool, or shed
        currrentState = models.CharField(max_length=20)
        timestamps = models.CharField(max_length=560)#CSV timestamps for every state
        workSpace = models.CharField(max_length=200)#for use in state machine
    """


def ProcessActions():

    #Re-process all action objects on every call
    for actionInstance in getAllActions():


        #states allow system to process and respond to all actions asyncrounusly

        #Tool borrow state machine
        if isToolRequest() == True: 
            if state == "userBorrowRequest":                                        #entry point
                #procede to next one
                actionInstance.currrentState = "askOwner"
                
                #re-invoke entire state machine

            if state == "askOwner":
                #generate question string asking [owner] if [borrower]
                
                question = "can " + actionInstance.requester.name + " borrow the " actionInstance.tool.name + "from " + actionInstance.tool.shed
                userOptions = ",Accept,Deny"                                                                  #adding questions           
                
                Notification.createResponseNotif(actionInstance,actionInstance.tool.owner,question,options=options,userOptions):

                #procede to next state
                pass
            elif state == "acceptDecline":

                #get notification assosiated with object
                    #if (notification responded == true):
                        #start timer for when tool is overdue (set end time)
                        #move tool location to requesters shed
                        #Continue to Borrowed state

                ownerResponse = Action.getAllActionNotifications(actionInstance)

                    #if notification responded fales - notify of denial and delete request

                pass
            elif state == "borrowed":
                #check if borrowed is past timestamp
                    #Notify {requester} that they are overdraft and they should return [tool]
                    #Set canBorrow state to false
                    #move to overdraft state

                #if (tool.isAvailable() == true):   #means tool has been returned
                    #move state to returned 

                pass
            elif state == "overDraft":
                #if (tool.isAvailable() == true):   #means tool has been returned
                    #calculate how many days the tool is overdue and reduce user reputation until then
                    #set user.canBorrow state to true.
                    #notify requester thankyou for returning the tool finally!
                    #move state to returned 

                pass
            elif state == "returned":
                #delete action object
                #Notify tool owner that his tool has been returned
                pass



        #shed request state machine

        if isShedRequest() == True:
            if state == "userShedRequest":
                #procede to next state
                pass
            elif state == "askAdmins":
                #loop through all admins of shed
                    #generate question string asking [Admin] if [borrower]

                    #proced to next state
                pass

            elif state == "acceptDecline":
                #get all notificaitons assosiated with this action
                    #check if notification has been responded to correctly

                pass
