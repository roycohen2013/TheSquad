from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed, Notification
import utilities.toolUtilities as toolUtils
import utilities.profileUtilities as profUtils
import utilities.shedUtilities as shedUtils
import utilities.notificationUtilities as notifUtils
import utilities.actionUtilities as actUtils
import os
import platform
import sys


import unittest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")

# Recomended command to run to see all tests
# python manage.py test toolCloudApp.tests -v 2


class actionTests (TestCase):
	fixtures = ["initDBData.json"]
	def setUp (self):
		self.genBorrowReq = actUtils.createBorrowRequestAction (Tool.objects.get (name = "Hoe"), profUtils.getProfileFromUsername ("TaikhoomAttar"))
		self.genJoinReq = actUtils.createShedRequestAction (Shed.objects.get (name = "Taikhoom's Shed"), profUtils.getProfileFromUsername ("TaikhoomAttar"))
		
	def test_isToolRequest (self):
		self.assertTrue (actUtils.isToolRequest (self.genBorrowReq))
		self.assertFalse (actUtils.isToolRequest (self.genJoinReq))
		
	def test_isShedRequest (self):
		self.assertFalse (actUtils.isShedRequest (self.genBorrowReq))
		self.assertTrue (actUtils.isShedRequest (self.genJoinReq))
		
	def test_getAllActions (self):
		self.assertTrue ((self.genBorrowReq in actUtils.getAllActions()) and (self.genJoinReq in actUtils.getAllActions()))
		
	def test_getProfileAction (self):
		self.assertTrue ((self.genBorrowReq in actUtils.getProfileAction(profUtils.getProfileFromUsername ("TaikhoomAttar")))\
		 and (self.genJoinReq in actUtils.getProfileAction(profUtils.getProfileFromUsername ("TaikhoomAttar"))))
		
	def test_getShedActions (self):
		self.assertIn (self.genJoinReq, actUtils.getShedActions (Shed.objects.get (name = "Taikhoom's Shed")))
		
	def test_getToolActions (self):
		self.assertIn (self.genBorrowReq, actUtils.getToolActions(Tool.objects.get (name = "Hoe")))