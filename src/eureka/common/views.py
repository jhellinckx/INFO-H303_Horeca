from django.shortcuts import render

# Create your views here.

from login.views import *
from login.models import *

def index(request):
	context = user_context(request)
	user = context["user"]
	return render(request, 'common/base.html', context)
