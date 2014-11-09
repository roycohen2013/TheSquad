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


#@unittest.skip("skipping Notification tests")    #can be used for skipping past certain tests



class notificationTests (TestCase):
    fixtures = ["initDBData.json"]
    def setUp (self):
        try:
        	self.genInfoNotif = notifUtils.createInfoNotif (Tool.objects.get(name = "Hoe"), profUtils.getProfileFromUsername ("TaikhoomAttar"), "Synergy is love, synergy is life")
        except:
        	self.fail ("Error in info notification generation!")


    def test_notif_creation (self):
	    """
	    """
	    tool = Tool.objects.get(name = "Hoe")
	    
	    prof = profUtils.getProfileFromUsername ("TaikhoomAttar")
	    msg = "Synergy is love, synergy is life"
	    generation = notifUtils.createInfoNotif (tool, prof, msg)
	    self.assertEqual (tool, generation.source)
	    self.assertEqual (prof, generation.recipient)
	    self.assertEqual (msg, generation.content)
    
    def test_InfoNotificationGet(self):
        """
        Tests Info notification creation for all types
        """
        getNotif = Notification.objects.get(id = self.genInfoNotif.object_id) #make sure the notification was actually saved to the db

        
        self.assertEqual (self.genInfoNotif, getNotif) #make sure the reference in the db = the reference returned by the creation of the notification


    def test_InfoNotificationDeletion(self):
        """

        Tests Info notification Deletion for all types
        
        """
        notifUtils.deleteNotif (self.genInfoNotif)
        self.assertNotIn (self.genInfoNotif, Notification.objects.all())
        
        
    def test_InfoNotificationIsInfoNotification (self):
        """
        """
        self.assertTrue (notifUtils.isInfoNotif (self.genInfoNotif))
    
    def test_InfoNotificationIsNotReqNotification (self):
        """
        """
        self.assertFalse (notifUtils.isRequestNotif (self.genInfoNotif))
        
    def test_AllProfileNotifs (self):
        """
        """
        self.assertIn (self.genInfoNotif, notifUtils.getAllProfileNotifs (profUtils.getProfileFromUsername ("TaikhoomAttar")))
        
    def test_AllActivrProfileNotifs (self):
        """
        THIS NEEDS TO BE MODIFIED FOR RESPONSE NOTIFICATIONS
        """
        self.assertIn (self.genInfoNotif, notifUtils.getAllActiveProfileNotifs (profUtils.getProfileFromUsername ("TaikhoomAttar")))
        
    def test_getNotifRecipient (self):
        """
        """
        self.assertEqual (profUtils.getProfileFromUsername ("TaikhoomAttar"), notifUtils.getNotifRecip (self.genInfoNotif))
        
    def test_getNotifContent (self):
        """
        """
        self.assertEqual ("Synergy is love, synergy is life", notifUtils.getNotifContent (self.genInfoNotif))
        
    def test_getNotifSourceObject (self):
        """
        """
        print (notifUtils.getNotifSourceObject (self.genInfoNotif))
        print (Tool.objects.get (name = "Hoe"))
        self.assertEqual (Tool.objects.get (name = "Hoe"), notifUtils.getNotifSourceObject (self.genInfoNotif))
        
    def test_getNotifSourceType (self):
        """
        """
        self.assertEqual ("Tool", notifUtils.getNotifSourceType (self.genInfoNotif))
        
    def test_isNotifFromTool (self):
        """
        """
        self.assertTrue (notifUtils.isNotifFromTool (self.genInfoNotif))
    
    def test_isNotifFromShed (self):
        """
        """
        self.assertFalse (notifUtils.isNotifFromShed (self.genInfoNotif))
        
    def test_isNotifFromAction (self):
        """ 
        """
        self.assertFalse (notifUtils.isNotifFromAction (self.genInfoNotif))
    
    def test_isNotifFromProfile (self):
        """
        """
        self.assertFalse (notifUtils.isNotifFromProfile (self.genInfoNotif))
    

