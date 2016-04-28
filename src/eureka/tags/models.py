from django.db import models

class Tag(models.Model):
    name = models.CharField(primary_key=True, max_length=16)

    class Meta:
        managed = False
        db_table = 'Tag'

class Establishmenttags(models.Model):
    establishment = models.ForeignKey(Establishment)
    tag_name = models.ForeignKey('Tag', db_column='tag_name')
    user_name = models.ForeignKey('User', db_column='user_name')

    class Meta:
        managed = False
        db_table = 'EstablishmentTags'
        unique_together = (('establishment_id', 'tag_name', 'user_name'),)


