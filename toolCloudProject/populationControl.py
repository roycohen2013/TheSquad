"""
	Populates the database with THE SQUAD.
	All 6 members of the squad will have their own account, shed, and tools.
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from toolCloudApp.models import Profile, Tool, Shed
from django.contrib.auth.models import User
import django.db
import string
import random

#print("--> Populating Database...")

names = [ ['Jake', 'Dulin'] , ['Roy', 'Cohen'] , ['Alex', 'Bowen'] , \
			['Taikhoom', 'Attar'], ['Jackson', 'McMahon'] , ['Adam','Walsh'] ]

profileObjects = []

for x in range(len(names)):

	firstName = names[x][0]
	lastName = names[x][1]
	userName = firstName+lastName
	x = str(x)
	newProfile = Profile(user = User.objects.create_user(userName, userName+'@gmail.com', 'password'), \
						 phoneNumber = '0000000000', address = 'address', sharezone = '14623', \
						 status = 'status')
	newProfile.user.first_name = firstName
	newProfile.user.last_name = lastName
	newProfile.user.save()
	newProfile.save()
	profileObjects.append(newProfile)

	
shedNames = ["Jake's Shed", "Roy's Shed", "Alex's Shed", "Taikhoom's Shed", \
				"Jackson's Shed", "Adam's Shed"]

shedObjects = []

for x in range(len(shedNames)):

	newShed = Shed(name=shedNames[x], owner=profileObjects[x], location='location', \
					sharezone='14623', status='status')
	newShed.save()
	newShed.members.add(profileObjects[x])
	newShed.admins.add(profileObjects[x])
	newShed.save()
	shedObjects.append(newShed)


toolNames = ['Hammer','Wrench','Screwdriver','Hoe','Drill','Impact Wrench', \
		     'Shovel', 'Saw', 'Electric Screwdriver', 'Nail Gun']

toolObjects = []

for x in range(len(toolNames)):

	newTool = Tool(name = toolNames[x], description='description', location = 'location', \
					isAvailable = True, tags = 'tags')
	newTool.owner = profileObjects[x%len(profileObjects)]
	newTool.save()
	toolObjects.append(newTool)

#print("--> Database populated")
