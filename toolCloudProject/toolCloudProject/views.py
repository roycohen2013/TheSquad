#Views

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf




def login(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html',c)


def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = authenticate(username=username,password=password)

	if user is not None:
		login(request)

		return HttpResponseRedirect('/accounts/loggedin')
	else:
		return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
	return render_to_response('loggedin.html',{'full_name': request.user.username})


def invalid_login(request):
	return render_to_response('invalid_login.html')

def logout(request):
	logout(request)
	return HttpResponseRedirect('/accounts/logout.html')