from django.shortcuts import render, redirect
from models import *
from django.contrib import messages 
import bcrypt

# Create your views here.

def index(request):
	return render (request, 'index.html')

def success(request):
	context = {
		'first_name': User.objects.get(id=request.session['id']).first_name
	}
	return render (request, 'success.html', context)

def process(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		 for tag, error in errors.iteritems():
		 	messages.error(request, error, extra_tags=tag)
		 return redirect('/')
	first_name = request.POST['first_name']
	last_name = request.POST['last_name']
	email = request.POST['email']
	# birthday = request.POST['birthday']
	password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
	User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
	request.session['id'] = User.objects.get(email=email).id
	return redirect('/success')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		 for tag, error in errors.iteritems():
		 	messages.error(request, error, extra_tags=tag)
		 return redirect('/')
	email = request.POST['email']
	request.session['id'] = User.objects.get(email=email).id
	return redirect('/success')