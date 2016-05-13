from __future__ import unicode_literals

from django.db import models

class Request:
	def __init__(self, name, request):
		self.name = name
		self.request = request
