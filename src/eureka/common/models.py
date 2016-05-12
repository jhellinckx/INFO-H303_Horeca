from django.db import connection

class BaseDBManager(object):
	def fetch_dicts(self, cursor):
		columns = [col[0] for col in cursor.description]
		return [
		    dict(zip(columns, row))
		    for row in cursor.fetchall()
		]

	def fetch_dict(self, cursor):
		columns = [col[0] for col in cursor.description]
		return dict(zip(columns, cursor.fetchone()))