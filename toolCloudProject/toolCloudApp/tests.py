from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed
import utilities.toolUtilities as toolUtils
import utilities.profileUtilities as profUtils
import utilities.shedUtilities as shedUtils

# Create your tests here.


class toolTestCase (TestCase):
	def testToolUtils (self):
		with open("populationControl.py") as f:
			code = compile(f.read(), "populationControl", 'exec')
			exec(code)
		ngTool = toolUtils.createNewTool ("Lightsaber", "Please don't hurt yourself with this", profUtils.getAllProfiles()[3], "Jedi Temple", "http://www.bitrebels.com/wp-content/uploads/2012/12/led-lightsaber-role-playing-6.jpg", True, "", "")
		
		ncTool = Tool.objects.get (name = "Lightsaber")
		nhTool = Tool.objects.get (name = "Hammer")
		self.assertEqual (ngTool, ncTool) #make sure that the tool  pulled from the db is the same reference as the returned reference
		
		self.assertNotEqual (nhTool, ngTool)  #make sure the tool is not the same as another random tool
		
		self.assertEqual (toolUtils.getToolName (ncTool), "Lightsaber") #testing getToolName
		
		self.assertEqual (toolUtils.getToolDescription (ncTool), "Please don't hurt yourself with this") #testing getToolDescription
		
		toolUtils.updateToolName (ncTool, "Darksaber") #changing the name of the tool
		self.assertEqual (toolUtils.getToolName (ncTool), "Darksaber") #making sure that the new name is saved
		
		
		
class shedTestCase (TestCase):
	def testShedUtils (self):
		with open("populationControl.py") as f:
			code = compile(f.read(), "populationControl", 'exec')
			exec(code)
		genShed = shedUtils.createNewShed (profUtils.getAllProfiles()[3], "Lightsaber Tools", "Coruscant", "Jedi Temple", "open", 0) #create new shed
		getShed = Shed.objects.get (name = "Lightsaber Tools") #make sure the shed was actually saved to the db
		
		self.assertEqual (genShed, getShed) #make sure the reference in the db = the reference returned by the creation of the shed
		
		self.assertEqual (shedUtils.getShedName (getShed), "Lightsaber Tools") #make sure names match
		
		self.assertIn (getShed, shedUtils.getAllShedsInSharezone ("Jedi Temple")) #make sure the shed is returned when doing a query of all sheds in zone
		
		shedUtils.addMemberToShed (getShed, profUtils.getAllProfiles()[2])
		self.assertIn (profUtils.getAllProfiles()[2], shedUtils.getAllMembersOfShed ())  #adding a member and then making sure he's there
		
		shedUtils.removeMemberFromShed (getShed, profUtils.getAllProfiles()[2])
		self.assertNotIn (profUtils.getAllProfiles()[2], shedUtils.getAllMembersOfShed()) #taking him out and then making sure he's not there
		
	
	
class profileTestCase (TestCase):
	def testProfUtils (self):
		with open("populationControl.py") as f:
			code = compile(f.read(), "populationControl", 'exec')
			exec(code)
		genProfile = profUtils.createNewProfile ("Obi-Wan", "Kenobi", "ben", "ben@jedi.edu","satine", "0000000000", "Tatooine", "Jedi Temple", "active", "") #mk User
		getProfile = Profile.objects.get (address = "Tatooine") #make sure we can catch him from the db
		
		self.assertEqual (genProfile, getProfile)
		
		self.assertEqual (profUtils.getFirstName(getProfile), "Obi-Wan")  #make sure the name was actually saved as Obi-Wan
		
		profUtils.updateFirstName (genProfile, "Ben")
		self.assertEqual (profUtils.getFirstName(getProfile), "Ben") #change his name to Ben and then make sure it was saved
		
		rep = profUtils.getReputation(getProfile)
		profUtils.updateReputation (getProfile, 10)
		self.assertGreater (profUtils.getReputation (getProfile), rep)  #make sure his reputation updates
		
		

		
		
		
		
		

		