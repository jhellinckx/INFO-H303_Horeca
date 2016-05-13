from __future__ import unicode_literals

from django.db import models

class Request:
	def __init__(self, iD, name, request):
		self.iD = iD
		self.name = name
		self.request = request
