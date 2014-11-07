"""
These tests depend on Selenium and also expect you to have Firefox installed.
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import bytearray
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from toolCloudApp.models import Profile, Tool, Shed
import utilities.toolUtilities as toolUtils
import utilities.profileUtilities as profUtils
import utilities.shedUtilities as shedUtils

class useCaseTests:
	def testUC1 (self):
		driver = webdriver.Firefox ()
		driver.get ("http://localhost:8000")
		
		driver.find_element_by_id ("registerBtn").click() #Click the register button
		
		driver.find_element_by_id ("id_first_name").send_keys("Boromir") #Enter the name Boromir into the first name field
		driver.find_element_by_id ("id_last_name").send_keys("so Denethor") #enter the name so Denethor into the last name field
		
		driver.find_element_by_id ("id_username").send_keys("borofgondor") #enter a username into the field
		
		driver.find_element_by_id ("id_email").send_keys("captain@minastirith.gov") #enter an email
		
		driver.find_element_by_id ("id_password1").send_keys ("faramir") #enter password
		
		driver.find_element_by_id ("id_password2").send_keys ("faramir") #reenter password
		
		driver.find_element_by_id ("id_phone_number").send_keys ("0000000000")
		
		driver.find_element_by_id ("id_share_zone").send_keys ("Minas Tirith")
		
		driver.findElement(By.xpath("//*[@value='Sign Up']")).click()
		
		body=driver.findElement(By.tagName("body")).getText()
	
	def testUC8 (self):
		driver = webdriver.Firefox ()
		driver.get ("http://localhost:8000/tools/submit/")
		
		driver.find_element_by_id ("id_name").send_keys ("Anduril")
		
		driver.find_element_by_id ("id_description").send_keys ("The reforged blade that was broken")
		
		driver.find_element_by_id ("id_tags").send_keys  ("sword")
		
		driver.findElement(By.xpath("//*[@value='Submit Tool']")).click();
		
	def testUC4 (self):
		driver = webdriver.Firefox()
		driver.get ("http://localhost:8000/sheds/create/")
		
		driver.find_element_by_id ("id_name").send_keys ("Rivendell")
		
		driver.find_element_by_id ("id_sharezone").send_keys ("Elven Middle-Earth")
		
		driver.findElement(By.xpath("//*[@value='Create New Shed']")).click()