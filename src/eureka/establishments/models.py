from django.db import models

class Establishment(models.Model):
    name = models.CharField(max_length=16)
    address_street = models.CharField(max_length=64)
    address_number = models.SmallIntegerField()
    address_postcode = models.IntegerField()
    address_locality = models.CharField(max_length=32)
    gps_longitude = models.DecimalField(max_digits=12, decimal_places=8)
    gps_latitude = models.DecimalField(max_digits=12, decimal_places=8)
    phone_number = models.CharField(max_length=16)
    website = models.URLField(max_length=255, blank=True, null=True)
    creator_name = models.ForeignKey('User', db_column='creator_name')
    created_time = models.DateField()

    class Meta:
        managed = False
        db_table = 'Establishment'


class Bar(models.Model):
    smoking = models.BooleanField()
    snack = models.BooleanField()
    establishment = models.ForeignKey('Establishment', primary_key=True)

    class Meta:
        managed = False
        db_table = 'Bar'

class Hotel(models.Model):
    stars = models.SmallIntegerField()
    rooms_number = models.IntegerField()
    price_range = models.DecimalField(max_digits=6, decimal_places=2)
    establishment = models.ForeignKey(Establishment, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Hotel'


class Restaurant(models.Model):
    price_range = models.DecimalField(max_digits=6, decimal_places=2)
    banquet_capacity = models.IntegerField()
    take_away = models.BooleanField()
    delivery = models.BooleanField()
    establishment = models.ForeignKey(Establishment, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Restaurant'


class Restaurantclosures(models.Model):
    day = models.CharField(max_length=16)
    am = models.BooleanField()
    pm = models.BooleanField()
    establishment = models.ForeignKey(Establishment)

    class Meta:
        managed = False
        db_table = 'RestaurantClosures'
