from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed
import utilities.toolUtilities as toolUtils
import utilities.profileUtilities as profUtils
import utilities.shedUtilities as shedUtils

# Create your tests here.


class toolTests (TestCase):
	def testToolUtils (self):
		with open("populationControl.py") as f:
			code = compile(f.read(), "populationControl", 'exec')
			exec(code)
		try:
			ngTool = toolUtils.createNewTool ("Lightsaber", "Please don't hurt yourself with this", profUtils.getAllProfiles()[3], "Jedi Temple", "http://www.bitrebels.com/wp-content/uploads/2012/12/led-lightsaber-role-playing-6.jpg", True, "", "")
		except:
			self.fail("Error when generating new tool")

		ncTool = Tool.objects.get (name = "Lightsaber")
		nhTool = Tool.objects.get (name = "Hammer")
		self.assertEqual (ngTool, ncTool) #make sure that the tool  pulled from the db is the same reference as the returned reference
		ncTool = Tool.objects.get (name = "Lightsaber")
		
		self.assertNotEqual (nhTool, ngTool)  #make sure the tool is not the same as another random tool
		ncTool = Tool.objects.get (name = "Lightsaber")
		
		self.assertEqual (toolUtils.getToolName (ncTool), "Lightsaber") #testing getToolName
		ncTool = Tool.objects.get (name = "Lightsaber")
		
		self.assertEqual (toolUtils.getToolDescription (ncTool), "Please don't hurt yourself with this") #testing getToolDescription
		ncTool = Tool.objects.get (name = "Lightsaber")
		
		toolUtils.updateToolName (ncTool, "Darksaber") #changing the name of the tool
		self.assertEqual (toolUtils.getToolName (ncTool), "Darksaber") #making sure that the new name is saved
		ncTool = Tool.objects.get (name = "Darksaber")
		
		toolUtils.updateToolDescription (ncTool, "Darth Maul stole this from Mandalorians") #changing the description of the tool
		self.assertEqual (toolUtils.getToolDescription (ncTool), "Darth Maul stole this from Mandalorians") #making sure that the new description is saved
		ncTool = Tool.objects.get (name = "Darksaber")
		
		toolUtils.updateToolTags (ncTool, "tag") #changing the name of the tool
		self.assertEqual (toolUtils.getToolTags (ncTool), "tag") #making sure that the new name is saved
		ncTool = Tool.objects.get (name = "Darksaber")
		
		self.assertEqual (toolUtils.getToolOwner(ncTool), profUtils.getAllProfiles()[3])  #testing getOwner
		ncTool = Tool.objects.get (name = "Darksaber")
		
		self.assertIn (ncTool, toolUtils.getToolsBelongingToProfile(profUtils.getAllProfiles()[3]))  #testing getToolsBelongingToProfile
		ncTool = Tool.objects.get (name = "Darksaber")
		
		toolUtils.updateToolBorrower (ncTool, profUtils.getAllProfiles()[2])    #testing toolBorrower
		self.assertEqual (toolUtils.getToolBorrower (ncTool), profUtils.getAllProfiles()[2])
		ncTool = Tool.objects.get (name = "Darksaber")
		
		toolUtils.updateToolShed (ncTool, Shed.objects.all()[0])   #tesging updatetoolshed and gettoolshed
		self.assertEqual (toolUtils.getToolShed(ncTool), Shed.objects.all()[0])
		ncTool = Tool.objects.get (name = "Darksaber")
		
		toolUtils.updateToolLocation (ncTool, "Dune Sea")
		self.assertEqual (toolUtils.getToolLocation (ncTool), "Dune Sea")
		ncTool = Tool.objects.get (name = "Darksaber")
		
		toolUtils.updateToolCondition (ncTool, 5)
		self.assertEqual (5, toolUtils.getToolCondition (ncTool))
		ncTool = Tool.objects.get (name = "Darksaber")
		
		self.assertEqual (toolUtils.getBorrowedCount(ncTool), 0)
		toolUtils.incrementBorrowedCount (ncTool)
		ncTool = Tool.objects.get (name = "Darksaber")
		self.assertEqual (toolUtils.getBorrowedCount(ncTool), 1)
		
		self.assertEqual (toolUtils.getRequestedCount(ncTool), 0)
		toolUtils.incrementRequestedCount (ncTool)
		ncTool = Tool.objects.get (name = "Darksaber")
		self.assertEqual (toolUtils.getRequestedCount(ncTool), 1)
		
		self.assertIn (ncTool, toolUtils.getAllTools())
		
		self.assertIn (ncTool, toolUtils.getAllToolsInShed(Shed.objects.all()[0]))
		
		self.assertEqual(toolUtils.isToolAvailable(ncTool), True)
		toolUtils.updateToolAvailability (ncTool, False)
		
		
		
class shedTests (TestCase):
	def testShedUtils (self):
		with open("populationControl.py") as f:
			code = compile(f.read(), "populationControl", 'exec')
			exec(code)
		try:
			genShed = shedUtils.createNewShed (profUtils.getAllProfiles()[3], "Lightsaber Tools", "Coruscant", "Jedi Temple", "open") #create new shed
		except:
			self.fail ("Error when generating new shed")
		
		getShed = Shed.objects.get (name = "Lightsaber Tools") #make sure the shed was actually saved to the db
		
		self.assertEqual (genShed, getShed) #make sure the reference in the db = the reference returned by the creation of the shed
		
		self.assertEqual (shedUtils.getShedName (getShed), "Lightsaber Tools") #make sure names match
		
		self.assertIn (getShed, shedUtils.getAllShedsInSharezone ("Jedi Temple")) #make sure the shed is returned when doing a query of all sheds in zone
		
		shedUtils.addMemberToShed (getShed, profUtils.getAllProfiles()[2])
		self.assertIn (profUtils.getAllProfiles()[2], shedUtils.getAllMembersOfShed ())  #adding a member and then making sure he's there
		
		shedUtils.removeMemberFromShed (getShed, profUtils.getAllProfiles()[2])
		self.assertNotIn (profUtils.getAllProfiles()[2], shedUtils.getAllMembersOfShed()) #taking him out and then making sure he's not there
		
		self.assertIn (getShed, shedUtils.getAllShedsAllSharezones())
		
		shedUtils.updateLatitudeOfShed (shedObj)
		
		
		
		
		
		
	
	
class profileTests (TestCase):
	def testProfUtils (self):
		with open("populationControl.py") as f:
			code = compile(f.read(), "populationControl", 'exec')
			exec(code)
		try:
			genProfile = profUtils.createNewProfile ("Obi-Wan", "Kenobi", "ben", "ben@jedi.edu","satine", "0000000000", "Room 42, Jedi Temple Master's Quarters", "Jedi Temple", "active", "") #mk User
		except:
			self.fail ("Error while generating user")
			
		getProfile = Profile.objects.get (address = "Tatooine") #make sure we can catch him from the db
		
		self.assertEqual (genProfile, getProfile)
		
		self.assertEqual (profUtils.getFirstName(getProfile), "Obi-Wan")  #make sure the name was actually saved as Obi-Wan
		
		profUtils.updateFirstName (genProfile, "Ben")
		self.assertEqual (profUtils.getFirstName(getProfile), "Ben") #change his name to Ben and then make sure it was saved
		
		rep = profUtils.getReputation(getProfile)
		profUtils.updateReputation (getProfile, 10)
		self.assertGreater (profUtils.getReputation (getProfile), rep)  #make sure his reputation updates
		
		profUtils.updateLastName (genProfile, "General")
		self.assertEqual (profUtils.getLastName(getProfile), "General") #change his name to Ben and then make sure it was saved
		
		self.assertNotIn (getProfile, profUtils.getAllOtherProfilesInSharezone (getProfile))
		
		self.assertIn (getProfile, profUtils.getAllProfilesInSharezone ("14623"))
		
		self.assertEqual (profUtils.getProfileFromUser (profUtils.getUserOfProfile(genProfile)), genProfile)
		
		self.updateAddress (getProfile, "Hut, Dune Sea, near Mos Eisley, Tatooine")
		self.assertEqual (profUtils.getAddress (genProfile), "Hut, Dune Sea, near Mos Eisley, Tatooine")
		
		profUtils.updateSharezone (getProfile, "Sandpeople")
		self.assertEqual (profUtils.getSharezone (genProfile), "Sandpeople")
		
		
		profUtils.updateStatus (getProfile, "Exile")
		self.assertEqual (profUtils.getStatus (genProfile), "Exile")
		
		profUtils.updateEmail (getProfile, "ben@moseisley.org")
		self.assertEqual (profUtils.getEmail (genProfile), "ben@moseisley.org")
		
		profUtils.updatePhoneNumber (getProfile, "1111111111")
		self.assertEqual (profUtils.getPhoneNumber (genProfile), "1111111111")
		
		
		

		

		
		
		

		