from django.shortcuts import render, redirect
from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^process$', views.process),
	url(r'^login$', views.login),
	url(r'^success$', views.success)
]