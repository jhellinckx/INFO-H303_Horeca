#!/usr/bin/python
# -*- coding: UTF-8 -*-

import psycopg2
import datetime
import sys

def insertEstablishment(name, address_street, address_num, address_zip, address_city, address_longitude, address_latitude, tel, website, creator_name, creation_date):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "Establishment" (name, address_street, address_number, address_postcode, address_locality, gps_longitude, gps_latitude, phone_number, website, creator_name, created_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;'
	establishment_id = -1
	try:
		connection = psycopg2.connect("dbname=db_eureka")
		cursor = connection.cursor()
		cursor.execute(sql_query, (name, address_street, address_num, address_zip, address_city, address_longitude, address_latitude, tel, website, creator_name, creation_date))
		establishment_id = cursor.fetchone()[0]
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't add an Establishment: ", e)
	return establishment_id

def insertUserFunction(name, admin):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "User" (name, email, password, signup_date, is_admin) VALUES (%s,%s,%s,%s,%s);'
	try:
		cursor.execute(sql_query, (name, name+"xmlparser@xml.com", "xml", datetime.date(2001,9,11), admin))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't add an User: ", e)

def changeToAdmin(name):
	connection, cursor = initConnectionAndCursor()
	print("In change admin")
	sql_query = 'UPDATE "User" SET is_admin = %s WHERE name = %s;'
	try:
		cursor.execute(sql_query, (True, name))
		closures(connection, cursor)
	except:
		print("Error modifying admin status")

def insertAdmin(name):
	insertUserFunction(name, True)

def insertUser(name):
	insertUserFunction(name, False)

def insertCafe(smoking, snack, establishment_id):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "Bar" (smoking, snack, establishment_id) VALUES (%s,%s,%s);'
	try:
		cursor.execute(sql_query, (smoking, snack, establishment_id))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't add a Cafe/Bar" , e)

def insertComment(establishment_id, username, date, score, text):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "EstablishmentComment" (written_date, score, comment_text, user_name, establishment_id) VALUES (%s, %s, %s, %s, %s);'
	try:
		cursor.execute(sql_query, (date, score, text, username, establishment_id))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't add a comment" , e)

def insertTag(name):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "Tag" (name) VALUES (%s);'
	try:
		cursor.execute(sql_query, (name,))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't insert Tag: " , e)

def insertEstablishmentTags(establishment_id, name, username):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "EstablishmentTags" (establishment_id, tag_name, user_name) VALUES (%s, %s, %s);'
	try:
		cursor.execute(sql_query, (establishment_id, name, username))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't insert Establishment Tag: " , e)

def insertRestaurant(establishment_id, price_range, banquet_capacity, take_away, delivery):
	connection , cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "Restaurant" (price_range, banquet_capacity, take_away, delivery, establishment_id) VALUES (%s, %s, %s, %s, %s);'
	try:
		cursor.execute(sql_query, (price_range, banquet_capacity, take_away, delivery, establishment_id))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't insert Restaurant: " , e)

def insertRestaurantClosures(establishment_id, day, day_am, day_pm):
	connection, cursor = initConnectionAndCursor()
	sql_query = 'INSERT INTO "RestaurantClosures" (day, am, pm, establishment_id) VALUES (%s, %s, %s, %s);'
	try:
		cursor.execute(sql_query, (day, day_am, day_pm, establishment_id))
		closures(connection, cursor)
	except psycopg2.IntegrityError as e:
		print("Can't insert a Restaurant Closure:" , e)

def initConnectionAndCursor():
	try:
		connection = psycopg2.connect("dbname=db_eureka")
		cursor = connection.cursor()
	except:
		print("Can't connect to the DB")
	return connection, cursor

def closures(connection, cursor):
	connection.commit()
	cursor.close()
	connection.close()