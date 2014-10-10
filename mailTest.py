#!/usr/bin/python
# $Author: jpm4208 $ test
import smtplib

sender = 'thesquad.toolcloud@gmail.com'
receivers = ['tfa2773@rit.edu','rxc1931@rit.edu','mab2098@rit.edu','jad5366@rit.edu','jpm4208@g.rit.edu','adw7422@rit.edu']

message = """From:  ToolCloud <thesquad.toolcloud@gmail.com>
Subject: ToolCloud test message

This is testing the mail code
"""

try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.starttls()
   smtpObj.login('thesquad.toolcloud','hailthesynergy')
   smtpObj.sendmail(sender, receivers, message)         
   print ("Successfully sent email")
except SMTPException:
   print ("Error: unable to send email")
