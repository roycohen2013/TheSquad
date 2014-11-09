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


#@unittest.skip("skipping Profile tests")    #can be used for skipping past certain tests
class profileTests (TestCase):
    fixtures = ["initDBData.json"]

    def setUp (self):
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
        
    def test_getProfilefromUsername (self):
        """
        """
        self.assertEqual (self.getProfile, profUtils.getProfileFromUsername ("ben"))
        print (profUtils.getProfileFromUsername ("ben"))

                

