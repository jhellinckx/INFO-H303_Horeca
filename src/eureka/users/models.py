from django.db import models

class User(models.Model):
    name = models.CharField(primary_key=True, max_length=16)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=128)
    signup_date = models.DateTimeField()
    is_admin = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'User'

