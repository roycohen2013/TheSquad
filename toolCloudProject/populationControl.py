"""
	Populates the database with 10 random users, tools, and sheds.
	Passwords for all users are 'password'.
	Usernames go in the format User0, User1, User2, ...
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")
from toolCloudApp.models import Profile, Tool, Shed
from django.contrib.auth.models import User

print("--> Populating Database...")

tools = ['Hammer','Wrench','Screwdriver','Hoe','Drill','Impact Wrench','Shovel', \
			'Hammer','Wrench','Screwdriver']

for x in range(10):

	x = str(x)
	newProfile = Profile(user = User.objects.create_user('User'+x, x+'@gmail.com', 'password'), \
						 phoneNumber = x, address = x, sharezone = '14623' + x, status = 'New User' + x, \
						 preferences = 'Test' + x)
	newProfile.user.first_name = 'First'+x
	newProfile.user.last_name = 'Last'+x
	newProfile.user.save()
	newProfile.save()
	
	newShed = Shed(name = "Shed" + x, owner = newProfile, location = x, \
					sharezone = x, status = x, preferences = x)
	newShed.save()
	
	if (int(x) % 2 == 0):
		isToolAvailable = True
	else:
		isToolAvailable = False

	newTool = Tool(name = tools[int(x)], description = x, location = x, \
					isAvailable = isToolAvailable, preferences = x, \
					owner = newProfile, tags = x)
	newTool.save()
	
	
print("--> Database populated")