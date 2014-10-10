from django.conf.urls import patterns, url

from toolCloudApp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
