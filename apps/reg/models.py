from __future__ import unicode_literals

from django.db import models

import md5

import re

import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserValiation(models.Manager):
	def basic_validator(self, postData):
		errors={}
		if len(postData['first_name']) < 3:
			errors['first_name'] = 'First name needs to be longer than 2 characters'
		if len(postData['last_name']) < 3:
			errors['last_name'] = 'Last name needs to be longer than 2 characters'
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Email invalid'
		if len(postData['password']) < 9 or len(postData['password2']) < 9:
			errors['password'] = 'Password needs to be more secure'
		if postData['password'] != postData['password2']:
			errors['mismatch'] = 'Passwords do not match'
		if len(User.objects.filter(email=postData['email'])) != 0:
			errors['user_exists'] = 'Email already taken'
		return errors
	def login_validator(self, postData):
		errors = {}
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = 'Email invalid'
		if len(User.objects.filter(email=postData['email'])) == 0:
			errors['user_exists'] = 'Account does not exist'
		if len(User.objects.filter(email=postData['email'])) != 0:
			password = User.objects.get(email=postData['email']).password
			if bcrypt.checkpw(postData['password'].encode(), password.encode()) != True:
				errors['password'] = 'Invalid password bro'
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=245)
	last_name = models.CharField(max_length=245)
	email = models.CharField(max_length=245)
	password = models.CharField(max_length=245)
	created_at = models.DateTimeField(auto_now_add=True)
	def __repr__(self):
		return '<User object: {} {} {} {} {}>'.format(self.first_name, self.last_name, self.email, self.password, self.created_at)
	objects = UserValiation()
