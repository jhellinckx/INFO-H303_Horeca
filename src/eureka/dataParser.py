#!/usr/local/bin/python
# -*- coding: UTF-8 -*-

import xml.etree.ElementTree as ET
import dbInserter as DB
import datetime

ADMINS = []
USERS = []
TAGS = []

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def parseCafes():
	tree = ET.parse('xml/Cafes.xml')
	Cafes = tree.getroot()

	for cafe in Cafes.findall("Cafe"):
		parseCafesInfos(cafe)

def parseRestaurants():
	tree = ET.parse('xml/Restaurants.xml')
	Restaurants = tree.getroot()
	for restaurant in Restaurants.findall("Restaurant"):
		parseRestaurantsInfos(restaurant)

def parseEstablishmentsInfos(establishment):
	creator_name = establishment.get("nickname")
	if creator_name not in ADMINS:
		if creator_name not in USERS:
			DB.insertAdmin(creator_name)
			ADMINS.append(creator_name)
		else:                               #if user commented or tagged an establishment before creating one,
			DB.changeToAdmin(creator_name)  #he was created as User, need to set it as an admin
			USERS.remove(creator_name)
			ADMINS.append(creator_name)
	creation_date = stringToDateFormat(establishment.get("creationDate"))
	name = establishment.find("Informations/Name").text

	address = establishment.find("Informations/Address")
	address_street = address.find("Street").text
	address_num = int(''.join(c for c in address.find("Num").text if c.isdigit())) #to avoid letters in address_num
	address_zip = int(address.find("Zip").text)
	address_city = address.find("City").text
	address_longitude = float(address.find("Longitude").text)
	address_latitude = float(address.find("Latitude").text)

	tel = establishment.find("Informations/Tel").text
	website = None
	if establishment.find("Informations/Site") != None:
		website = establishment.find("Informations/Site").get("link")
	establishment_id = DB.insertEstablishment(name, address_street, address_num, address_zip, address_city, address_longitude, address_latitude, tel, website, creator_name, creation_date)
	return establishment_id

def parseCafesInfos(cafe):
	establishment_id = parseEstablishmentsInfos(cafe)
	smoking = (cafe.find("Informations/Smoking") != None)
	snack = (cafe.find("Informations/Snack") != None)

	DB.insertCafe(smoking, snack, establishment_id) #DB insertion

	parseComments(cafe, establishment_id)
	parseTags(cafe, establishment_id)

def parseRestaurantsInfos(restaurant):
	establishment_id = parseEstablishmentsInfos(restaurant)
	price_range = restaurant.find("Informations/PriceRange").text
	banquet_capacity = restaurant.find("Informations/Banquet").get("capacity")
	take_away = (restaurant.find("Informations/TakeAway") != None)
	delivery = (restaurant.find("Informations/Delivery") != None)

	DB.insertRestaurant(establishment_id, price_range, banquet_capacity, take_away, delivery)

	parseRestaurantClosures(restaurant, establishment_id)
	parseComments(restaurant, establishment_id)
	parseTags(restaurant, establishment_id)

def parseComments(establishment, establishment_id):
	for comment in establishment.findall("Comments/Comment"):
		username = comment.get("nickname")
		if username not in (ADMINS and USERS):
			DB.insertUser(username)
			USERS.append(username)
		date = stringToDateFormat(comment.get("date"))
		score = comment.get("score")
		text = comment.text
		DB.insertComment(establishment_id, username, date, score, text)

def parseTags(establishment, establishment_id):
	for tag in establishment.findall("Tags/Tag"):
		name = tag.get("name")
		if name not in TAGS:
			DB.insertTag(name)
			TAGS.append(name)
		for user in tag.findall("User"):
			username = user.get("nickname")
			if username not in (ADMINS and USERS):
				DB.insertUser(username)
				USERS.append(username)
			DB.insertEstablishmentTags(establishment_id, name, username)

def parseRestaurantClosures(restaurant, establishment_id):
	parsed_days = []
	for day in restaurant.findall("Informations/Closed/On"):
		day_am, day_pm = True,True  #If no attribute "hour" present in closure, means closed all day
		if day.get("hour") == "pm": 
			day_am = False #means it is only closed for PM (so AM = False)
		elif day.get("hour") == "am":
			day_pm = False
		parsed_days.append(DAY_NAMES[int(day.get("day"))])
		DB.insertRestaurantClosures(establishment_id, DAY_NAMES[int(day.get("day"))], day_am, day_pm)
	for day in DAY_NAMES :
		if day not in parsed_days:
			DB.insertRestaurantClosures(establishment_id, day, False, False)

def stringToDateFormat(dateString):
	dateString = dateString.split("/")
	if len(dateString) == 3:
		return datetime.date(int(dateString[2]), int(dateString[1]), int(dateString[0]))
	else:
		return datetime.date(2001,9,11) #If error in XML parsin, putting a default value: 9/11

if __name__ == "__main__":
	parseCafes()
	parseRestaurants()