 #!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404, HttpResponseRedirect
from django.db import connection

from establishments.models import *
from login.models import User
from .models import Request

R1Name = "Tous les utilisateurs qui apprécient au moins 3 établissements que l’utilisateur 'Brenda' apprécie."
R1 = '''
SELECT u.name FROM "User" u WHERE 3<= (SELECT count(ec2.user_name) FROM "EstablishmentComment" ec2 WHERE u.name = ec2.user_name AND ec2.score >= 4 AND ec2.establishment_id IN (SELECT DISTINCT e.id FROM "Establishment" e, "EstablishmentComment" ec WHERE e.id = ec.establishment_id AND ec.user_name = 'Brenda' and ec.score >= 4));
'''

R2Name = "Tous les établissements qu’apprécie au moins un utilisateur qui apprécie tous les établissements que 'Brenda' apprécie."
R2 = '''
SELECT e2.id FROM "Establishment" e2 WHERE EXISTS (SELECT * FROM "EstablishmentComment" ec4 WHERE e2.id = ec4.establishment_id AND ec4.score>=4 AND ec4.user_name IN (SELECT u.name FROM "User" u WHERE (SELECT count(ec3.user_name) FROM "EstablishmentComment" ec3 WHERE ec3.user_name = 'Brenda' and ec3.score >=4 ) = (SELECT count(ec2.user_name) FROM "EstablishmentComment" ec2 WHERE u.name = ec2.user_name AND ec2.score >= 4 AND ec2.establishment_id IN (SELECT DISTINCT e.id FROM "Establishment" e, "EstablishmentComment" ec WHERE e.id = ec.establishment_id AND ec.user_name = 'Brenda' and ec.score >= 4))));
'''

R3Name = "Tous les établissements pour lesquels il y a au plus un commentaire."
R3 = '''
SELECT e.id FROM "Establishment" e WHERE (SELECT count(ec.establishment_id) FROM "EstablishmentComment" ec WHERE ec.establishment_id = e.id) <= 1;
'''

R4Name = "La liste des administrateurs n’ayant pas commenté tous les établissements qu’ils ont crées."
R4 = '''
SELECT DISTINCT u.name FROM "User" u, "Establishment" e WHERE u.is_admin = 't' AND e.creator_name = u.name AND NOT EXISTS (SELECT * FROM "EstablishmentComment" ec WHERE ec.establishment_id = e.id AND ec.user_name = u.name);
'''

R5Name = "La liste des établissements ayant au minimum trois commentaires, classée selon la moyenne des scores attribués."
R5 = '''
SELECT e.id FROM "Establishment" e, "EstablishmentComment" ec WHERE e.id = ec.establishment_id GROUP BY (e.id) HAVING count(ec.establishment_id) >= 3 ORDER BY avg(ec.score) DESC;
'''

REQUESTS = [Request(R1Name,R1), Request(R2Name, R2), Request(R3Name, R3), Request(R4Name, R4), Request(R5Name, R5)]

def index_requests(request):
	context = {'requests' : REQUESTS}
	return render(request, 'dbrequests/index_requests.html', context)