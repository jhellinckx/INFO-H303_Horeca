from django.db import connection
from common.models import BaseDBManager

class CommentDBManager(BaseDBManager):
    def get_by_establishment(self, establishment_id):
        with connection.cursor() as c:
            c.execute('SELECT written_date, score, comment_text, user_name, establishment_id FROM "EstablishmentComment" WHERE establishment_id = %s;', [establishment_id])
            return [EstablishmentComment.from_db(d) for d in self.fetch_dicts(c)]

    def get_by_user(self, user):
        pass


class EstablishmentComment(object):

    db = CommentDBManager()

    def __init__(self, establishment_id, written_date, score, comment_text, user_name):
        self.establishment_id = establishment_id
        self.written_date = written_date
        self.score = score
        self.comment_text = comment_text
        self.user_name = user_name
        
    @classmethod
    def from_db(cls, db_dict):
        return cls(db_dict["establishment_id"], db_dict["written_date"], db_dict["score"], \
            db_dict["comment_text"], db_dict["user_name"])