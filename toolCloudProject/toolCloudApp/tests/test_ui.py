"""
These tests depend on Selenium and also expect you to have Firefox installed.
"""

import sys
sys.path.append("selenium")
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed
from time import sleep # just for debugging -- so I can see where the browser is before it dies
import utilities.profileUtilities as profUtils

import unittest


#@unittest.skip("skipping UI tests tests")    #can be used for skipping past certain tests
class UITests (LiveServerTestCase):
	fixtures = ['initDBData.json']
	
	def setUp(self):
		self.selenium = webdriver.Firefox()
		try:
			self.selenium.get (self.live_server_url + "/accounts/login/")
			self.selenium.find_element_by_id ("username").send_keys ("TaikhoomAttar")
			self.selenium.find_element_by_id ("password").send_keys ("password")
			self.selenium.find_element_by_xpath("//*[@value='login']").click()
		except:
			self.selenium.quit()
			self.fail ("Error accessing site")
			
		
	def tearDown (self):
		self.selenium.quit()
		
		
	def test_registration (self):
		self.selenium.get (self.live_server_url + "/accounts/logout/")
		self.selenium.get (self.live_server_url + "/accounts/register/")
		WebDriverWait(self.selenium, 2).until(
		lambda driver: driver.find_element_by_tag_name('body'))
			
		self.selenium.find_element_by_id ("id_first_name").send_keys("Boromir") #Enter the name Boromir into the first name field
		self.selenium.find_element_by_id ("id_last_name").send_keys("so Denethor") #enter the name so Denethor into the last name field
			
		self.selenium.find_element_by_id ("id_username").send_keys("borofgondor") #enter a username into the field
		
		self.selenium.find_element_by_id ("id_email").send_keys("captain@minastirith.gov") #enter an email
		
		self.selenium.find_element_by_id ("id_password1").send_keys ("faramir") #enter password
		
		self.selenium.find_element_by_id ("id_password2").send_keys ("faramir") #reenter password
		
		self.selenium.find_element_by_id ("id_phone_number").send_keys ("0000000000")
		
		self.selenium.find_element_by_id ("id_share_zone").send_keys ("Minas Tirith")
		
		self.selenium.find_element_by_xpath("//*[@value='Sign Up']").click()

		try:
			Profile.objects.get (sharezone = "Minas Tirith")
		except:
			self.fail ("New user not saved!")
		
			
	def test_tool_creation (self):
		self.selenium.get (self.live_server_url + "/tools/submit/")
		
		self.selenium.find_element_by_id ("id_name").send_keys ("Anduril")
		
		self.selenium.find_element_by_id ("id_description").send_keys ("The reforged blade that was broken")
		
		self.selenium.find_element_by_id ("id_tags").send_keys  ("sword")
		
		self.selenium.find_element_by_xpath("//*[@value='Submit Tool']").click()

		try:
			Tool.objects.get (name = "Anduril")
		except:
			self.fail ("New tool not saved!")
			
			
	def test_shed_creation (self):
		self.selenium.get (self.live_server_url + "/sheds/create/")
		
		self.selenium.find_element_by_id ("id_name").send_keys ("Rivendell")
		
		self.selenium.find_element_by_id ("id_sharezone").send_keys ("Elven")
		
		self.selenium.find_element_by_xpath("//*[@value='Create New Shed']").click()
		try:
			Shed.objects.get (name = "Rivendell")
		except:
			self.fail ("New shed not saved!")
	
	
