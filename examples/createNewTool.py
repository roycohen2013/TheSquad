"""
$Date $
$Revision $
$Author $
"""

from django.contrib.auth.models import User
from toolCloudApp.models import Profile, Tool, Shed
from django.utils import timezone

"""This script will create a new tool object (from Squad models)

called during tool submittal from frontend

UNFINISHED

written by Jackson and Roy
"""

def newTool(name, description, ownerID):
	toolObject = Tool()