from django.db import connection
from django.db import IntegrityError
from common.models import BaseDBManager
import time
class EstablishmentDBManager(BaseDBManager):

    def get_all(self):
        with connection.cursor() as c:
            c.execute('SELECT * FROM \"' + self.model().table + '\" JOIN "Establishment" ON id=establishment_id;')
            return [self.model().from_db(d) for d in self.fetch_dicts(c)]

    def get_by_id(self, establishment_id):
        with connection.cursor() as c:
            c.execute('SELECT * FROM \"' + self.model().table + '\" JOIN "Establishment" ON id=establishment_id WHERE establishment_id=%s;', [establishment_id])
            d = self.fetch_dict(c)
            return self.model().from_db(d) if d != None else None

    def create_establishment_from_dict(self, form_dict, username):
        created_time = time.strftime('%Y-%m-%d %H:%M:%S')
        creator_name = username
        try:
            with connection.cursor() as c:
                c.execute('INSERT INTO "Establishment" (name, address_street, address_number, address_postcode, address_locality, gps_longitude, gps_latitude, phone_number, website, creator_name, created_time) \
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;',
                    [
                        form_dict["name"],
                        form_dict["address_street"],
                        form_dict["address_number"],
                        form_dict["address_postcode"],
                        form_dict["address_locality"],
                        form_dict["gps_longitude"],
                        form_dict["gps_latitude"],
                        form_dict["phone_number"],
                        form_dict["website"],
                        creator_name,
                        created_time
                    ])
                return c.fetchone()[0]
        except IntegrityError as e:
            return -1

    def edit_establishment_from_dict(self, form_dict, establishment_id):
        try:
            with connection.cursor() as c:
                c.execute('UPDATE "Establishment" SET name=%s, address_street=%s, address_number=%s, \
                    address_postcode=%s, address_locality=%s, gps_longitude=%s, gps_latitude=%s,\
                    phone_number=%s, website=%s WHERE id=%s;',
                    [
                        form_dict["name"],
                        form_dict["address_street"],
                        form_dict["address_number"],
                        form_dict["address_postcode"],
                        form_dict["address_locality"],
                        form_dict["gps_longitude"],
                        form_dict["gps_latitude"],
                        form_dict["phone_number"],
                        form_dict["website"],
                        establishment_id
                    ])
        except IntegrityError as e:
            return False
        return True

    def model(self):
        raise NotImplementedError


class HotelDBManager(EstablishmentDBManager):
    def model(self):
        return Hotel

    def create_from_dict(self, form_dict, username):
        establishment_id = self.create_establishment_from_dict(form_dict, username)
        if establishment_id == -1:
            return (False, establishment_id)
        else:
            try:
                with connection.cursor() as c:
                    c.execute('INSERT INTO "Hotel" (stars, rooms_number, price_range, establishment_id)\
                        VALUES (%s, %s, %s, %s);',
                        [
                            form_dict["stars"],
                            form_dict["rooms_number"],
                            form_dict["price_range"],
                            establishment_id
                        ])
            except IntegrityError as e:
                return (False, establishment_id)
        return (True, establishment_id)

    def edit_from_dict(self, form_dict, establishment_id):
        success = self.edit_establishment_from_dict(form_dict, establishment_id)
        if not success :
            return False
        else:
            try:
                with connection.cursor() as c:
                    c.execute('UPDATE "Hotel" SET stars=%s, rooms_number=%s, price_range=%s WHERE establishment_id=%s;',
                        [
                            form_dict["stars"],
                            form_dict["rooms_number"],
                            form_dict["price_range"],
                            establishment_id
                        ])
            except IntegrityError as e:
                return False
        return True


class BarDBManager(EstablishmentDBManager):
    def model(self):
        return Bar

    def create_from_dict(self, form_dict, username):
        establishment_id = self.create_establishment_from_dict(form_dict, username)
        if establishment_id == -1:
            return (False, establishment_id)
        else:
            try:
                with connection.cursor() as c:
                    c.execute('INSERT INTO "Bar" (smoking, snack, establishment_id)\
                        VALUES (%s, %s, %s);',
                        [
                            form_dict["smoking"],
                            form_dict["snack"],
                            establishment_id
                        ])
            except IntegrityError as e:
                return (False, establishment_id)
        return (True, establishment_id)

    def edit_from_dict(self, form_dict, establishment_id):
        success = self.edit_establishment_from_dict(form_dict, establishment_id)
        if not success :
            return False
        else:
            try:
                with connection.cursor() as c:
                    c.execute('UPDATE "Bar" SET smoking=%s, snack=%s WHERE establishment_id=%s;',
                        [
                            form_dict["smoking"],
                            form_dict["snack"],
                            establishment_id
                        ])
            except IntegrityError as e:
                return False
        return True

class RestaurantDBManager(EstablishmentDBManager):
    def model(self):
        return Restaurant

    def create_from_dict(self, form_dict, username):
        establishment_id = self.create_establishment_from_dict(form_dict, username)
        if establishment_id == -1:
            return (False, establishment_id)
        else:
            try:
                with connection.cursor() as c:
                    c.execute('INSERT INTO "Restaurant" (price_range, banquet_capacity, take_away, delivery, establishment_id)\
                        VALUES (%s, %s, %s, %s, %s);',
                        [
                            form_dict["price_range"],
                            form_dict["banquet_capacity"],
                            form_dict["take_away"],
                            form_dict["delivery"],
                            establishment_id
                        ])
            except IntegrityError as e:
                return (False, establishment_id)
        return (True, establishment_id)

    def edit_from_dict(self, form_dict, establishment_id):
        success = self.edit_establishment_from_dict(form_dict, establishment_id)
        if not success :
            return False
        else:
            try:
                with connection.cursor() as c:
                    c.execute('UPDATE "Restaurant" SET price_range=%s, banquet_capacity=%s, take_away=%s, delivery=%s\
                        WHERE establishment_id=%s;',
                        [
                            form_dict["price_range"],
                            form_dict["banquet_capacity"],
                            form_dict["take_away"],
                            form_dict["delivery"],
                            establishment_id
                        ])
            except IntegrityError as e:
                return False
        return True


class Establishment(object):

    table = 'Establishment'
 
    def populate(self, db_dict):
        self.name = db_dict["name"]
        self.address_street = db_dict["address_street"]
        self.address_number = db_dict["address_number"]
        self.address_postcode = db_dict["address_postcode"]
        self.address_locality = db_dict["address_locality"]
        self.gps_longitude = db_dict["gps_longitude"]
        self.gps_latitude = db_dict["gps_latitude"]
        self.phone_number = db_dict["phone_number"]
        self.website = db_dict["website"]
        self.creator_name = db_dict["creator_name"]
        self.created_time = db_dict["created_time"]

class Hotel(Establishment):

    table = 'Hotel'
    db = HotelDBManager()

    def __init__(self, establishment_id, stars, rooms_number, price_range, db_dict):
        self.establishment_id = establishment_id
        self.stars = stars
        self.rooms_number = rooms_number
        self.price_range = price_range
        self.db_dict = db_dict

    @classmethod
    def from_db(cls, db_dict):
        hotel = cls(db_dict["establishment_id"], db_dict["stars"], db_dict["rooms_number"], db_dict["price_range"], db_dict) 
        hotel.populate(db_dict)
        return hotel

    def get_dict(self):
        return self.db_dict
        


class Bar(Establishment):

    table = 'Bar'
    db = BarDBManager()

    def __init__(self, establishment_id, smoking, snack, db_dict):
        self.establishment_id = establishment_id
        self.smoking = smoking
        self.snack = snack
        self.db_dict = db_dict

    @classmethod
    def from_db(cls, db_dict):
        bar = cls(db_dict["establishment_id"], db_dict["smoking"], db_dict["snack"], db_dict)
        bar.populate(db_dict)
        return bar

    def get_dict(self):
        return self.db_dict


class Restaurant(Establishment):

    table = 'Restaurant'
    db = RestaurantDBManager()

    def __init__(self, establishment_id, price_range, banquet_capacity, take_away, delivery, db_dict):
        self.establishment_id = establishment_id
        self.price_range = price_range
        self.banquet_capacity = banquet_capacity
        self.take_away = take_away
        self.delivery = delivery
        self.db_dict = db_dict

    @classmethod
    def from_db(cls, db_dict):
        restaurant = cls(db_dict["establishment_id"], db_dict["price_range"], db_dict["banquet_capacity"], \
            db_dict["take_away"], db_dict["delivery"], db_dict)
        restaurant.populate(db_dict)
        return restaurant

    def get_dict(self):
        return self.db_dict


class RestaurantClosuresDBManager(BaseDBManager):
    def get_by_establishment(self, establishment_id):
        with connection.cursor() as c :
            c.execute('SELECT day, am, pm, establishment_id FROM "RestaurantClosures" WHERE establishment_id = %s', [establishment_id])
            return [RestaurantClosures.from_db(d) for d in self.fetch_dicts(c)]

class RestaurantClosures(object):
    
    db = RestaurantClosuresDBManager()

    def __init__(self, establishment_id, day, am, pm):
        self.establishment_id = establishment_id
        self.day = day
        self.am = am
        self.pm = pm

    @classmethod
    def from_db(cls, db_dict):
        return cls(db_dict["establishment_id"], db_dict["day"], db_dict["am"], db_dict["pm"])


    
