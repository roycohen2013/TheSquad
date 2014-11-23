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
 
