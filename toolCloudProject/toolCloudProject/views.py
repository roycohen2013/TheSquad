#Views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.context_processors import csrf
from utilities import content




def login(request):
	c = {}
	c.update(csrf(request))
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
	return render_to_response('userHome.html',content.genUserHome(request))


def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	auth_logout(request)
	return render_to_response('logout.html')