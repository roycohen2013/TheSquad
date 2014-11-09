









# load action object

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

#Tool borrow state machine

if state ==	"userBorrowRequest":
	#procede to next one
    pass
elif state == "askOwner":
	#generate question string asking [owner] if [borrower]

	#procede to next state
    pass
elif state == "acceptDecline":
	#get notification assosiated with object
		#if (notification responded == true):
			#start timer for when tool is overdue (set end time)
			#move tool location to requesters shed
			#Continue to Borrowed state


		#if notification responded fales - notify of denial and delete request

    pass
elif state == "borrowed":
	#check if borrowed is past timestamp
		#Notify {requester} that they are overdraft and they should return [tool]
		#Set canBorrow state to false
		#move to overdraft state
    pass
elif state == "overDraft":
	#once 
    pass
elif state == "returned":
    pass



#shed request state machine


if state ==	"userShedRequest":
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
