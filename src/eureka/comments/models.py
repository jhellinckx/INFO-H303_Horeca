from django.db import models

class Establishmentcomment(models.Model):
    written_date = models.DateTimeField()
    score = models.SmallIntegerField()
    comment_text = models.TextField()
    user_name = models.ForeignKey('User', db_column='user_name')
    establishment = models.ForeignKey(Establishment)

    class Meta:
        managed = False
        db_table = 'EstablishmentComment'
        unique_together = (('written_date', 'user_name', 'establishment_id'),)

