# NAME: NewSlate
"""
$LastChangedDate: 2014-10-05 14:36:43 -0400 (Sun, 05 Oct 2014) $
$Rev: 51 $
$Author: rxc1931 $

"""


#run SVN update
#!/usr/bin/env python
import os
import sys
import platform
from subprocess import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "toolCloudProject.settings")

from django.conf import settings
from django.core import management
from django.contrib.auth.models import User

print ("========== NEW SLATE PROGRAM INITIATING ==========")
print ("")

# Get the arguments list 
#cmdargs = str(sys.argv)
total = len(sys.argv)
mode = 1 					#default arguments list

if total > 1:
	if sys.argv[1]== "1":
		mode = 1 			#full automatic mode
	elif sys.argv[1]== "2":
		mode = 2			#newslate with no repopulation
else:
	mode = 1 			#full automatic mode selected in case no arguments passed


if mode == 1:
	print ("--> Full automatic mode selected")
elif mode == 2:
	print ("--> minimal Newslate mode selected")


print ("-->	Collecting static files...")
#os.system('manage.py collectstatic')
management.call_command('collectstatic',interactive=False)
print ("-->	Static files collected")


print ("-->	Deleting old database file...")
os.system('rm db.sqlite3')
print ("-->	Delete Complete")

print ("")

print ("-->	DataBase syncronization starting...")
management.call_command('syncdb', interactive=False)
print ("-->DataBase sync Complete")

print ("")


print ("--> flushing database...")
management.call_command('flush', interactive=False)
print ("--> Database flush complete")

print ("")


print ("--> Generating root user...")
u = User(username='root')
u.set_password('root')
u.is_superuser = True
u.is_staff = True
u.save()
print ("--> User generation complete")

print ("")

if mode == 1:
	if platform.system() == 'Linux' or platform.system() == 'Darwin':
		os.system('python3 populationControl.py')
	else:
		os.system('python populationControl.py')
	print("")




print ("========== NEW SLATE PROGRAM COMPLETE ==========")

SquadName = """\
   _____  ____  _    _         _____  
  / ____|/ __ \| |  | |  /\   |  __ \ 
 | (___ | |  | | |  | | /  \  | |  | |
  \___ \| |  | | |  | |/ /\ \ | |  | |
  ____) | |__| | |__| / ____ \| |__| |
 |_____/ \___\_\\____/_/    \_\_____/ 
                                      
"""

print(SquadName)

print ("Have a nice day friend :)")

                             



#call(["pythonPath","manage.py",'flush'," --username=root","--email=thesquad.toolcloud@gmail.com"])	#flush command to wipe db


#call(["pythonPath","manage.py","createsuperuser"])
#    execute_from_command_line("pythonPath","manage.py",'flush',"--noinput","--no-initial-data"])


#execute_from_command_line(["flush","--noinput","--no-initial-data"])


# u = User(username='root')
# u.set_password('root')
# u.is_superuser = True
# u.is_staff = True
# u.save()

