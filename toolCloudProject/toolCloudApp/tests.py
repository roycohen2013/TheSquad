from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed, Notification
import utilities.toolUtilities as toolUtils
import utilities.profileUtilities as profUtils
import utilities.shedUtilities as shedUtils
import utilities.notificationUtilities as notifUtils
import os
import platform
import sys


import unittest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")

# Recomended command to run to see all tests
# python manage.py test toolCloudApp.tests -v 2




#@unittest.skip("skipping Tool tests")    #can be used for skipping past certain tests
class toolTests (TestCase):
    fixtures = ["initDBData.json"]



    def setUp (self):
        #with open("populationControl.py") as f:
        #    code = compile(f.read(), "populationControl", 'exec')
        #    exec(code)
        try:

            self.ngTool = toolUtils.createNewTool ("Lightsaber", "Please don't hurt yourself with this", profUtils.getAllProfiles()[3], "Jedi Temple", "http://www.bitrebels.com", True, "", "")
            self.ncTool = Tool.objects.get (name = "Lightsaber")
            self.nhTool = Tool.objects.get (name = "Hammer")

                   
        except:
            self.fail ("Error while generating new tool")


    def test_GetTool(self):
        """
        """
        self.assertEqual (self.ngTool, self.ncTool) #make sure that the tool  pulled from the db is the same reference as the returned reference

        self.assertNotEqual (self.nhTool, self.ngTool)  #make sure the tool is not the same as another random tool

    def test_GetToolName(self):
        """
        """
        self.assertEqual(toolUtils.getToolName (self.ncTool), "Lightsaber") #testing getToolName

    def test_GetToolDescription(self):
        """
        """
        self.assertEqual (toolUtils.getToolDescription(self.ncTool), "Please don't hurt yourself with this") #testing getToolDescription

    def test_GetToolName(self):
        """
        """
        toolUtils.updateToolName (self.ncTool, "Darksaber") #changing the name of the tool
        self.assertEqual (toolUtils.getToolName (self.ncTool), "Darksaber") #making sure that the new name is saved
  

    def test_UpdateToolDescription(self):
        """
        """
        toolUtils.updateToolDescription (self.ncTool, "Darth Maul stole this from Mandalorians") #changing the description of the tool
        self.assertEqual(toolUtils.getToolDescription (self.ncTool), "Darth Maul stole this from Mandalorians") #making sure that the new description is saved

    def test_updateToolTags(self):
        """
        """
        toolUtils.updateToolTags (self.ncTool, "tag") #changing the name of the tool
        self.assertEqual (toolUtils.getToolTags (self.ncTool), "tag") #making sure that the new name is saved

    def test_GetToolTags(self):
        """
        """
        self.assertEqual (toolUtils.getToolTags (self.ncTool), "") #making sure that the new name is saved

    def test_GetToolsBelongingToProfile(self):
        """
        """
        self.assertIn (self.ncTool, toolUtils.getToolsBelongingToProfile(profUtils.getAllProfiles()[3]))  #testing getToolsBelongingToProfile

    def test_GetToolBorrower(self):
        """
        """
        self.assertEqual(toolUtils.getToolBorrower(self.ncTool), None)  #initial state has no borrowers



    def test_UpdateToolBorrower(self):
        """
        """
        toolUtils.updateToolBorrower (self.ncTool, profUtils.getAllProfiles()[2])    #testing toolBorrower
        self.assertEqual (toolUtils.getToolBorrower (self.ncTool), profUtils.getAllProfiles()[2])


    def test_getToolShed(self):
        """
        """
        self.assertEqual (toolUtils.getToolShed(self.ncTool), None)



    def test_UpdateToolShed(self):
        """
        """
        toolUtils.updateToolShed (self.ncTool, Shed.objects.all()[0])   #tesging updatetoolshed and gettoolshed
        self.assertEqual (toolUtils.getToolShed(self.ncTool), Shed.objects.all()[0])
 

    def test_GetToolLocation(self):
        """
        """
        self.assertEqual (toolUtils.getToolLocation (self.ncTool), "Jedi Temple")


    def test_UpdateToolLocation(self):
        """
        """
        toolUtils.updateToolLocation (self.ncTool, "Dune Sea")
        self.assertEqual (toolUtils.getToolLocation (self.ncTool), "Dune Sea")


    def test_GetToolCondition(self):
        """
        """
        self.assertEqual (0, toolUtils.getToolCondition (self.ncTool))  #default value is 0



    def test_UpdateToolCondition(self):
        """
        """
        toolUtils.updateToolCondition (self.ncTool, 5)
        self.assertEqual (5, toolUtils.getToolCondition (self.ncTool))



    def test_GetBorrowedCount(self):
        """
        """
        self.assertEqual (toolUtils.getBorrowedCount(self.ncTool), 0)


    def test_IncrimentBorrowedCount(self):
        """
        """
        self.assertEqual (toolUtils.getBorrowedCount(self.ncTool), 0)
        toolUtils.incrementBorrowedCount (self.ncTool)
        self.assertEqual (toolUtils.getBorrowedCount(self.ncTool), 1)


    def test_GetRequestedCount(self):
        """
        """
        self.assertEqual (toolUtils.getRequestedCount(self.ncTool), 0)


    def test_IncrimentRequestedCount(self):
        """
        """
        self.assertEqual (toolUtils.getRequestedCount(self.ncTool), 0)
        toolUtils.incrementRequestedCount (self.ncTool)
        self.assertEqual (toolUtils.getRequestedCount(self.ncTool), 1)


    def test_GetAllTools(self):
        """
        """
        self.assertIn (self.ncTool, toolUtils.getAllTools())


    def test_GetAllToolsInShed(self):
        """
        """
        self.assertIn (self.ncTool, toolUtils.getAllToolsInShed(toolUtils.getToolShed(self.ncTool)))


    def test_IsToolAvailability(self):
        """
        """
        self.assertEqual(toolUtils.isToolAvailable(self.ncTool), True)
        toolUtils.updateToolAvailability (self.ncTool, False)
        self.assertEqual(toolUtils.isToolAvailable(self.ncTool), False)

    def test_UpdateToolAvailability(self):
        """
        """
        toolUtils.updateToolAvailability (self.ncTool, False)
        self.assertEqual(toolUtils.isToolAvailable(self.ncTool), False)
        toolUtils.updateToolAvailability (self.ncTool, True)
        self.assertEqual(toolUtils.isToolAvailable(self.ncTool), True)



        
        
#@unittest.skip("skipping Shed tests")    #can be used for skipping past certain tests   
class shedTests (TestCase):
    fixtures = ["initDBData.json"]

    def setUp (self):

        #with open("populationControl.py") as f:
        #    code = compile(f.read(), "populationControl", 'exec')
        #    exec(code)
        try:

            self.genShed = shedUtils.createNewShed (profUtils.getAllProfiles()[3], "Lightsaber Tools", "Jedi Temple", "Coruscant", "open") #create new shed
            self.getShed = getShed = Shed.objects.get (name = "Lightsaber Tools") #make sure the shed was actually saved to the db
        
        except:
            self.fail ("Error while generating shed")

    def test_CreateNewShed(self):
        """
        """



    def test_GetShed(self):
        """
        """
        self.assertEqual (self.genShed, self.getShed) #make sure the reference in the db = the reference returned by the creation of the shed

   
    def test_GetAllShedsInSharezone(self):
        """
        """
        self.assertIn (self.getShed, shedUtils.getAllShedsInSharezone ("Coruscant")) #make sure the shed is returned when doing a query of all sheds in zone

    def test_GetAllMembersOfShed(self):
        """
        """
        #print (shedUtils.getAllMembersOfShed(self.getShed))

        self.assertEqual(0, len(shedUtils.getAllMembersOfShed(self.getShed)))    # this shed should have no people added yet

        self.getShed = Shed.objects.get(name = "Jake's Shed")

        self.assertIn (profUtils.getAllProfiles()[3], shedUtils.getAllMembersOfShed (self.getShed))  #Check if jake is in his own shed



    def test_AddMemberToShed(self):
        """
        """
        shedUtils.addMemberToShed (self.getShed, profUtils.getAllProfiles()[2])
        getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertIn (profUtils.getAllProfiles()[2], shedUtils.getAllMembersOfShed (self.getShed))  #adding a member and then making sure he's there
 
    def test_GetAllShedsAllSharezones(self):
        """
        """
        self.assertIn (self.getShed, shedUtils.getAllShedsAllSharezones())



    def test_RemoveMemberFromShed(self):
        """
        """
        shedUtils.removeMemberFromShed (self.getShed, profUtils.getAllProfiles()[2])
        self.getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertNotIn (profUtils.getAllProfiles()[2], shedUtils.getAllMembersOfShed(self.getShed)) #taking him out and then making sure he's not there
 

    def test_GetLatitudeOfShed(self):
        """
        """
        self.assertEqual (shedUtils.getLatitudeOfShed (self.getShed), -1)

    def test_GetLongitudeOfShed(self):
        """
        """
        self.assertEqual (shedUtils.getLongitudeOfShed (self.getShed), -1)


    def test_UpdateLatitudeOfShed(self):
        """
        """
        shedUtils.updateLatitudeOfShed (self.getShed, 45)
        getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertEqual (shedUtils.getLatitudeOfShed (self.getShed), 45)

   
    def test_UpdateLongitudeOfShed(self):
        """
        """
        shedUtils.updateLongitudeOfShed (self.getShed, 55)
        self.getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertEqual (shedUtils.getLongitudeOfShed (self.getShed), 55)

    def test_GetLocationOfShed(self):
        """
        """
        self.assertEqual (shedUtils.getLocationOfShed (self.getShed), "Jedi Temple")

    def test_UpdateLocationOfShed(self):
        """
        """
        shedUtils.updateLocationOfShed (self.getShed, "Emperor Palpatine's personal stronghold")
        self.getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertEqual (shedUtils.getLocationOfShed (self.getShed), "Emperor Palpatine's personal stronghold")
        
    def test_GetShareZoneOfShed(self):
        """
        """
        self.assertEqual(shedUtils.getSharezoneOfShed (self.getShed), "Coruscant")

    def test_GetOwnerOfShed(self):
        """
        """
        self.assertEqual(shedUtils.getOwnerOfShed (self.getShed), profUtils.getAllProfiles()[3])

    def test_GetNameOfShed(self):
        """
        """
        self.assertEqual(shedUtils.getNameOfShed (self.getShed), "Lightsaber Tools") #make sure names match

    def test_UpdateNameOfShed(self):
        """
        """
        shedUtils.updateNameOfShed (self.getShed,"Jedi artifacts")
        self.getShed = Shed.objects.get (name = "Jedi artifacts")
        self.assertEqual (shedUtils.getNameOfShed (self.getShed), "Jedi artifacts")


    def test_AddAdminToShed(self):
        """
        """
        shedUtils.addAdminToShed (self.getShed, profUtils.getAllProfiles()[2])
        self.getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertIn (profUtils.getAllProfiles()[2], shedUtils.getAllAdminsOfShed (self.getShed))  #adding an admin and then making sure he's there

    def test_RemoveAdminFromShed(self):
        shedUtils.removeAdminFromShed (self.getShed, profUtils.getAllProfiles()[2])
        self.getShed = Shed.objects.get (name = "Lightsaber Tools")
        self.assertNotIn (profUtils.getAllProfiles()[2], shedUtils.getAllAdminsOfShed(self.getShed)) #taking him out and then making sure he's not there
 
        
        
        
    
#@unittest.skip("skipping Profile tests")    #can be used for skipping past certain tests
class profileTests (TestCase):
    fixtures = ["initDBData.json"]


    def setUp (self):

        #with open("populationControl.py") as f:
        #    code = compile(f.read(), "populationControl", 'exec')
        #    exec(code)
        try:

            self.genProfile = profUtils.createNewProfile ("Obi-Wan", "Kenobi", "ben", "ben@jedi.edu","satine", "0000000000", "Room 42, Jedi Temple Master's Quarters", "Jedi Temple", "active", 0) #mk User
            
            self.getProfile = Profile.objects.get (address = "Room 42, Jedi Temple Master's Quarters") #make sure we can catch him from the db
        
        except:
            self.fail ("Error while generating user")


    def test_GetProfile(self):
        """
        tests that GetProfile returns same profile as submitted to database
        """
        self.assertEqual (self.genProfile, self.getProfile)


    def test_GetFirstName(self):
        """

        """
        self.assertEqual(profUtils.getFirstName(self.getProfile), "Obi-Wan")  #make sure the name was actually saved as Obi-Wan

    def test_GetLastName(self):
        """

        """
        self.assertEqual(profUtils.getLastName(self.getProfile), "Kenobi")  #make sure the name was actually saved as Obi-Wan



    def test_UpdateFirstName(self):
        """

        """
        profUtils.updateFirstName (self.getProfile, "Ben")
        self.assertEqual (profUtils.getFirstName(self.getProfile), "Ben") #change his name to Ben and then make sure it was saved

    def test_UpdateLastName(self):
        """

        """
        profUtils.updateLastName (self.getProfile, "General")
        self.assertEqual (profUtils.getLastName(self.getProfile), "General") #change his name to Ben and then make sure it was saved


    def test_GetReputation(self):
        """
        """
        self.assertEqual (profUtils.getReputation(self.getProfile), 50) #change his name to Ben and then make sure it was saved

    def test_UpdateReputation(self):
        rep = profUtils.getReputation(self.getProfile)
        profUtils.updateReputation(self.getProfile, 10)
        self.assertGreater (profUtils.getReputation(self.getProfile), rep)  #make sure his reputation updates

    def test_GetAllOtherProfilesInSharezone(self):
        """
        """
        self.assertNotIn (self.getProfile, profUtils.getAllOtherProfilesInSharezone(self.getProfile))


    def test_GetAllProfilesInShareZone(self):
        """
        """
        self.assertIn(self.getProfile, profUtils.getAllProfilesInSharezone("Jedi Temple"))

    def test_GetUserOfProfile(self):
        """
        """
        self.assertEqual(profUtils.getProfileFromUser(profUtils.getUserofProfile(self.genProfile)), self.genProfile)

    def test_GetAddress(self):
        """
        """
        self.assertEqual (profUtils.getAddress(self.getProfile), "Room 42, Jedi Temple Master's Quarters")

    def test_UpdateAddress(self):
        """
        """
        profUtils.updateAddress (self.getProfile, "Hut, Dune Sea, near Mos Eisley, Tatooine")
        self.assertEqual (profUtils.getAddress (self.getProfile), "Hut, Dune Sea, near Mos Eisley, Tatooine")


    def test_GetShareZone(self):
        """
        """
        self.assertEqual (profUtils.getSharezone(self.getProfile), "Jedi Temple")

    def test_UpdateShareZone(self):
        """
        """
        profUtils.updateSharezone(self.getProfile, "Sandpeople")
        self.assertEqual (profUtils.getSharezone(self.getProfile), "Sandpeople")


    def test_GetStatus(self):
        """
        """
        self.assertEqual (profUtils.getStatus (self.getProfile), "active")

    def test_UpdateStatus(self):
        """
        """
        profUtils.updateStatus (self.getProfile, "Exile")
        self.assertEqual(profUtils.getStatus(self.getProfile), "Exile")


    def test_GetEmail(self):
        """
        """
        self.assertEqual (profUtils.getEmail (self.getProfile), "ben@jedi.edu")

    def test_UpdateEmail(self):
        """
        """
        profUtils.updateEmail(self.getProfile, "ben@moseisley.org")
        self.assertEqual (profUtils.getEmail(self.getProfile), "ben@moseisley.org")
   
    def test_GetPhoneNumber(self):
        """
        """
        self.assertEqual (profUtils.getPhoneNumber (self.getProfile), "0000000000")

    def test_UpdatePhoneNumber(self):
        """
        """
        profUtils.updatePhoneNumber (self.getProfile, "1111111111")
        self.assertEqual (profUtils.getPhoneNumber(self.getProfile), "1111111111")

                

        
#@unittest.skip("skipping Notification tests")    #can be used for skipping past certain tests
class notificationTests (TestCase):
    fixtures = ["initDBData.json"]
    def setUp (self):
        # if platform.system() == 'Linux' or platform.system() == 'Darwin':
        #     os.system('python3 populationControl.py')
        # else:
        #     os.system('python populationControl.py')
        # print("")
        #with open("populationControl.py") as f:
        #    code = compile(f.read(), "populationControl", 'exec')
        #    exec(code)
        try:
            self.genShed = shedUtils.createNewShed (profUtils.getAllProfiles()[3], "shed notification test", "somwhere ", "somezone", "open") #create new shed
        
            self.RecptProfile = profUtils.createNewProfile ("some", "Person", "somePerson122", "somePerson122@toolcloud.com",\
                                                  "password", "2012227555", "someAddress", "someZones", "active", 0) #mk User

            self.genTool = toolUtils.createNewTool ("Lightsaber", "Please don't hurt yourself with this", profUtils.getAllProfiles()[3], "Jedi Temple", "http://www.bitrebels.com", True, "", "")
 
            #RecptProfile = profUtils.createNewProfile ("Obi-Wan", "Kenobi", "ben", "ben@jedi.edu","satine", "0000000000", "Room 42, Jedi Temple Master's Quarters", "Jedi Temple", "active", 0) #mk User
        except:
            self.fail ("Error while generating user")
                
       
            

    def test_InfoNotificationCreation(self):
        """
        Tests Info notification creation for all types
        """
        
        #self.genShed = shedUtils.createNewShed (profUtils.getAllProfiles()[3], "shed notification test", "somwhere ", "somezone", "open") #create new shed
        #RecptProfile = profUtils.createNewProfile ("some", "Person", "somePerson122", "somePerson122@toolcloud.com",\
        #                                          "password", "2012227555", "someAddress", "someZones", "active", 0) #mk User

        genNotif = notifUtils.createNotificationInfo(self.genShed, self.RecptProfile, "test Content")
        getNotif = Notification.objects.get(id = genNotif.object_id) #make sure the shed was actually saved to the db

        
        self.assertEqual (genNotif, getNotif) #make sure the reference in the db = the reference returned by the creation of the shed


    def test_InfoNotificationDeletion(self):
        """

        Tests Info notification Deletion for all types
        
        """
        pass

