from django.db import connection
from common.models import BaseDBManager

class EstablishmentDBManager(BaseDBManager):

    def get_all(self):
        with connection.cursor() as c:
            c.execute('SELECT * FROM \"' + self.model().table + '\" JOIN "Establishment" ON id=establishment_id;')
            return [self.model().from_db(d) for d in self.fetch_dicts(c)]

    def get_by_id(self, establishment_id):
        with connection.cursor() as c:
            c.execute('SELECT * FROM \"' + self.model().table + '\" JOIN "Establishment" ON id=establishment_id WHERE establishment_id=%s;', [establishment_id])
            return self.model().from_db(self.fetch_dict(c))

    def model(self):
        raise NotImplementedError


class HotelDBManager(EstablishmentDBManager):
    def model(self):
        return Hotel


class BarDBManager(EstablishmentDBManager):
    def model(self):
        return Bar

class RestaurantDBManager(EstablishmentDBManager):
    def model(self):
        return Restaurant

class RestaurantClosuresDBManager(BaseDBManager):
    pass

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

    def __init__(self, establishment_id, stars, rooms_number, price_range):
        self.establishment_id = establishment_id
        self.stars = stars
        self.rooms_number = rooms_number
        self.price_range = price_range

    @classmethod
    def from_db(cls, db_dict):
        hotel = cls(db_dict["establishment_id"], db_dict["stars"], db_dict["rooms_number"], db_dict["price_range"]) 
        hotel.populate(db_dict)
        return hotel
        


class Bar(Establishment):

    table = 'Bar'
    db = BarDBManager()

    def __init__(self, establishment_id, smoking, snack):
        self.establishment_id = establishment_id
        self.smoking = smoking
        self.snack = snack

    @classmethod
    def from_db(cls, db_dict):
        bar = cls(db_dict["establishment_id"], db_dict["smoking"], db_dict["snack"])
        bar.populate(db_dict)
        return bar


class Restaurant(Establishment):

    table = 'Restaurant'
    db = RestaurantDBManager()

    def __init__(self, establishment_id, price_range, banquet_capacity, take_away, delivery):
        self.establishment_id = establishment_id
        self.price_range = price_range
        self.banquet_capacity = banquet_capacity
        self.take_away = take_away
        self.delivery = delivery

    @classmethod
    def from_db(cls, db_dict):
        restaurant = cls(db_dict["establishment_id"], db_dict["price_range"], db_dict["banquet_capacity"], \
            db_dict["take_away"], db_dict["delivery"])
        restaurant.populate(db_dict)
        return restaurant



class RestaurantClosures(object):
    pass
    # day = models.CharField(max_length=16)
    # am = models.BooleanField()
    # pm = models.BooleanField()
    # establishment = models.ForeignKey(Establishment)

    
