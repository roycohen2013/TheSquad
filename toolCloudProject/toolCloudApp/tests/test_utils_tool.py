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


