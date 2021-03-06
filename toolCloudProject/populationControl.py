"""
	Populates the database with THE SQUAD.
	All 6 members of the squad will have their own account, shed, and tools.
	Also adds an account for Al.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from toolCloudApp.models import Profile, Tool, Shed
from django.contrib.auth.models import User
import django.db
import string
import random

names = [ ['Al', 'Arujunan'] , ['Jake', 'Dulin'] , ['Roy', 'Cohen'] , ['Alex', 'Bowen'] , \
			['Taikhoom', 'Attar'], ['Jackson', 'McMahon'] , ['Adam','Walsh'] ]
emails = ["2manyhats@gmail.com", "jad5366@g.rit.edu", "rxc1931@gmail.com", "mab2098@g.rit.edu", \
			"tfa2773@g.rit.edu", "jpm4208@g.rit.edu", "adw7422@g.rit.edu"]
phoneNumbers = ["1234567890", "2032097215", "9176905094", "2404697313", "2482292139", \
			"3154805597", "6176803278"]

profileObjects = []

for x in range(len(names)):

	firstName = names[x][0]
	lastName = names[x][1]
	userName = firstName+lastName
	email = emails[x]
	pn = phoneNumbers[x]
	x = str(x)
	newProfile = Profile(user = User.objects.create_user(userName, email, 'password'), \
						 phoneNumber = pn, streetAddress = '1 Lomb Memorial Drive', sharezone = '14623', \
						 city = 'Rochester', state = 'NY', stateName = 'New York', \
						 status = 'status')
	newProfile.user.first_name = firstName
	newProfile.user.last_name = lastName
	newProfile.user.save()
	if userName == "AlArujunan":
		newProfile.emailNotifs == False
		newProfile.textNotifs == False
	newProfile.save()
	profileObjects.append(newProfile)

	
shedNames = ["AlArujunan's Shed", "JakeDulin's Shed", "RoyCohen's Shed", "AlexBowen's Shed", "TaikhoomAttar's Shed", \
				"JacksonMcMahon's Shed", "AdamWalsh's Shed"]

shedObjects = []

for x in range(len(shedNames)):

	newShed = Shed(name=shedNames[x], owner=profileObjects[x], location=profileObjects[x].streetAddress + \
		", " + profileObjects[x].city + ", " + profileObjects[x].state + " " + profileObjects[x].sharezone, \
					sharezone=profileObjects[x].sharezone, status='status')
	newShed.save()
	newShed.members.add(profileObjects[x])
	newShed.admins.add(profileObjects[x])
	newShed.save()
	profileObjects[x].personalShed = newShed
	profileObjects[x].save()
	shedObjects.append(newShed)


toolNames = ['Claw Hammer','Wrench','Screwdriver','Hoe','Drill','Impact Wrench', \
		     'Shovel', 'Hand Saw', 'Electric Screwdriver', 'Nail Gun', '3D Printer', 'Heat Gun', \
		     'Circular Saw', 'Nibbler', 'Belt Sander', 'Chainsaw', 'Hedge clippers', 'Pressure Washer',
		     'Wet Vacuum', 'Shamwow', 'Tile Saw', 'Socket Wrench', 'Sledgehammer', 'Reciprocating Saw']

toolObjects = []

for x in range(len(toolNames)):

	newTool = Tool(name = toolNames[x], description='description', \
					isAvailable = True, tags = 'tags')
	newTool.owner = profileObjects[x % len(profileObjects)]
	newTool.myShed = shedObjects[x % len(shedObjects)]
	newTool.location = newTool.myShed.location
	newTool.save()
	toolObjects.append(newTool)

#print("--> Database populated")
