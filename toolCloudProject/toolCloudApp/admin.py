from django.contrib import admin
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
import django.db
from toolCloudApp.models import Profile, User, Notification, Action
from toolCloudApp.mailSend import sendMail
import string
import random

"""
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(1,parentdir) 
"""
import utilities.profileUtilities as profileUtil
import utilities.shedUtilities as shedUtil
import utilities.toolUtilities as toolUtil
import utilities.notificationUtilities as notifUtil
import utilities.actionUtilities as actionUtil
import utilities.content as content

# Register your models here.
from toolCloudApp.forms import debugForm

def debug(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = debugForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            cd = form.cleaned_data.get ("a")
            cd = "from toolCloudApp.models import Profile, Tool, Shed\n" + cd
            code = compile(cd, "test", 'exec')
            exec (code)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = debugForm()

    return render(request, 'debug_view.html', {'form': form})