#Views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.context_processors import csrf
from utilities import content
from utilities import notificationUtilities as notifUtil
from utilities import profileUtilities as profileUtil




def login(request):
	c = {}
	c.update(csrf(request))
	c.update(content.genSuper())
	return render_to_response('login.html',c)


def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = authenticate(username=username,password=password)

	if user is not None:
		auth_login(request,user)
		return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
	return render_to_response('userHome.html', content.genUserHome(request))


def invalid_login(request):
	c = {}
	c.update(csrf(request))
	c.update(content.genFailedLogin())
	return render_to_response('login.html', c)

def logout(request):
	auth_logout(request)
	return render_to_response('logout.html', content.genSuper())