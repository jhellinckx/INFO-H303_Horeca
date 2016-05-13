from django.db import connection
from django.db import IntegrityError
from common.models import BaseDBManager
import time 

class UserDBManager(BaseDBManager):
	def get_all(self):
		with connection.cursor() as c:
			c.execute('SELECT * FROM "User"')
			return [User.from_db(d) for d in self.fetch_dicts(c)]

	def get_with_password(self, username, password):
		with connection.cursor() as c:
			c.execute('SELECT * FROM "User" WHERE name=%s AND password=%s', [username, password])
			d = self.fetch_dict(c)
			return User.from_db(d) if d != None else None

	def get(self, username):
		with connection.cursor() as c:
			c.execute('SELECT * FROM "User" WHERE name=%s', [username])
			d = self.fetch_dict(c)
			return User.from_db(d) if d != None else None


	def create_user(self, name, email, password, is_admin=False):
		date = time.strftime('%Y-%m-%d %H:%M:%S')
		#is_admin = str(int(is_admin))
		with connection.cursor() as c:
			try:
				c.execute('INSERT INTO "User" VALUES(%s, %s, %s, %s, %s)',[name, email, password, date, is_admin])
			except IntegrityError as e:
				return False
		return True

	def edit_from_dict(self, form_dict, username):
		try:
			with connection.cursor() as c:
				c.execute('UPDATE "User" SET name=%s, email=%s, password=%s, is_admin=%s WHERE name=%s;',
					[
						form_dict["username"],
						form_dict["email"],
						form_dict["password"],
						form_dict["is_admin"],
						username
					])
		except IntegrityError as e:
			return False
		return True

class User(object):

	db = UserDBManager()

	def __init__(self, name, email, password, signup_date, is_admin, db_dict):	
		self.name = name
		self.email = email
		self.password = password
		self.signup_date = signup_date
		self.is_admin = is_admin
		self.db_dict = db_dict

	@classmethod
	def from_db(cls, db_dict):
		return cls(db_dict["name"], db_dict["email"], db_dict["password"], \
			db_dict["signup_date"], db_dict["is_admin"], db_dict)

	def get_dict(self):
		return self.db_dict












