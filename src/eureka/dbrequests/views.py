 #!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.db import connection

from common.models import BaseDBManager


from establishments.models import *
from login.models import User
from .models import Request
from login.views import *

R1Name = "R1: Tous les utilisateurs qui apprécient au moins 3 établissements que l’utilisateur 'Brenda' apprécie."
R1 = '''
SELECT u.name FROM "User" u WHERE 3<= (SELECT count(ec2.user_name) FROM "EstablishmentComment" ec2 WHERE u.name = ec2.user_name AND ec2.score >= 4 AND ec2.establishment_id IN (SELECT DISTINCT e.id FROM "Establishment" e, "EstablishmentComment" ec WHERE e.id = ec.establishment_id AND ec.user_name = 'Brenda' and ec.score >= 4));'''

R2Name = "R2: Tous les établissements qu’apprécie au moins un utilisateur qui apprécie tous les établissements que 'Brenda' apprécie."
R2 = '''
SELECT e2.id FROM "Establishment" e2 WHERE EXISTS (SELECT * FROM "EstablishmentComment" ec4 WHERE e2.id = ec4.establishment_id AND ec4.score>=4 AND ec4.user_name IN (SELECT u.name FROM "User" u WHERE (SELECT count(ec3.user_name) FROM "EstablishmentComment" ec3 WHERE ec3.user_name = 'Brenda' and ec3.score >=4 ) = (SELECT count(ec2.user_name) FROM "EstablishmentComment" ec2 WHERE u.name = ec2.user_name AND ec2.score >= 4 AND ec2.establishment_id IN (SELECT DISTINCT e.id FROM "Establishment" e, "EstablishmentComment" ec WHERE e.id = ec.establishment_id AND ec.user_name = 'Brenda' and ec.score >= 4))));'''

R3Name = "R3: Tous les établissements pour lesquels il y a au plus un commentaire."
R3 = '''
SELECT e.id FROM "Establishment" e WHERE (SELECT count(ec.establishment_id) FROM "EstablishmentComment" ec WHERE ec.establishment_id = e.id) <= 1;'''

R4Name = "R4: La liste des administrateurs n’ayant pas commenté tous les établissements qu’ils ont crées."
R4 = '''
SELECT DISTINCT u.name FROM "User" u, "Establishment" e WHERE u.is_admin = 't' AND e.creator_name = u.name AND NOT EXISTS (SELECT * FROM "EstablishmentComment" ec WHERE ec.establishment_id = e.id AND ec.user_name = u.name);'''

R5Name = "R5: La liste des établissements ayant au minimum trois commentaires, classée selon la moyenne des scores attribués."
R5 = '''
SELECT e.id FROM "Establishment" e, "EstablishmentComment" ec WHERE e.id = ec.establishment_id GROUP BY (e.id) HAVING count(ec.establishment_id) >= 3 ORDER BY avg(ec.score) DESC;'''

REQUESTS_USERS = [Request(1,R1Name,R1), Request(4,R4Name, R4)]
REQUESTS_ESTABLISHMENTS = [Request(2,R2Name, R2),  Request(3,R3Name, R3), Request(5,R5Name, R5)]

def index_requests(request):
	context = user_context(request)
	context['requests_users'] = REQUESTS_USERS
	context['requests_establishments'] = REQUESTS_ESTABLISHMENTS
	return render(request, 'dbrequests/index_requests.html', context)


def establishments_request_detail(request, request_id):
	context = user_context(request)
	sqlQuery = ''' '''
	for dbrequest in REQUESTS_ESTABLISHMENTS:
		if dbrequest.iD == int(request_id):
			sqlQuery = dbrequest.request
	context["title"] = "Request results"
	with connection.cursor() as c:
		manager = BaseDBManager()
		restaurantQuery = ''' SELECT * FROM "Restaurant" r JOIN "Establishment" ON "Establishment".id=r.establishment_id WHERE r.establishment_id IN (''' + sqlQuery[:len(sqlQuery)-1] + ''');'''
		c.execute(restaurantQuery)
		context["all_restaurants_list"] = [Restaurant.from_db(d) for d in manager.fetch_dicts(c)]

		barQuery = ''' SELECT * FROM "Bar" b JOIN "Establishment" ON "Establishment".id=b.establishment_id WHERE b.establishment_id IN (''' + sqlQuery[:len(sqlQuery)-1] + ''');'''
		c.execute(barQuery)
		context["all_bars_list"] = [Bar.from_db(d) for d in manager.fetch_dicts(c)]

		hotelQuery = ''' SELECT * FROM "Hotel" h JOIN "Establishment" ON "Establishment".id=h.establishment_id WHERE h.establishment_id IN (''' + sqlQuery[:len(sqlQuery)-1] + ''');'''
		c.execute(hotelQuery)
		context["all_hotel_list"] = [Hotel.from_db(d) for d in manager.fetch_dicts(c)]

	return render(request, 'establishments/index.html', context)
