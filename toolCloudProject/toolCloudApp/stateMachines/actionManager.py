









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
    pass
elif state == "askOwner":
	#generate question string asking [owner] if [borrower]

    pass
elif state == "acceptDecline":
    pass
elif state == "pickup":
    pass
elif state == "borrowed":
    pass
elif state == "overDraft":
    pass
elif state == "returned":
    pass



#shed request state machine


if state ==	"userShedRequest":
    pass
elif state == "askAdmins":
	#loop through all admins of shed
		#generate question string asking [Admin] if [borrower]


	

    pass
elif state == "acceptDecline":
    pass
elif state == "pickup":
