from django.db import models
from django.db import connection
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)

class EurekaUserManager(BaseUserManager):
	def create_user(self, name, email, password, signup_date, is_admin=False):
		check_required(name, email, password, signup_date)

		user = self.model(
			email=self.normalize_email(email),
			signup_date=signup_date,
			is_admin=False,
		)
		user.set_password(password)

		return user

	def check_required(self, name, email, password, signup_date):
		if not name:
			raise ValueError("Users must have an username")
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		if not signup_date:
			raise ValueError("Users must have a signup date")

	def raw_get(self, username):
		try:
			return raw("SELECT * FROM User WHERE name = %s;", [username])[0]
		except IndexError :
			return None


class EurekaUser(AbstractBaseUser):
	name = models.CharField(primary_key=True, max_length=16)
	email = models.EmailField(unique=True, max_length=255)
	signup_date = models.DateTimeField()
	is_admin = models.BooleanField()
	
	class Meta:
		managed = False
		db_table = 'User'
	
	objects = EurekaUserManager()
	
	USERNAME_FIELD = "name"
	
	def get_full_name(self):
		return name
	
	def get_short_name(self):
		return name
	
	def __str__(self):
		return name

class EurekaAuthBackend(object):
	def authenticate(self, username=None, password=None):
		user = EurekaUser.objects.raw_get(username)
