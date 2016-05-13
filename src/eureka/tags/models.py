from django.db import connection
from common.models import BaseDBManager

class TagDBManager(BaseDBManager):
    
    def get_all(self):
        with connection.cursor() as c:
            c.execute('SELECT * FROM "Tag";')
            return [Tag.from_db(d) for d in self.fetch_dicts(c)]

class EstablishmentTagDBManager(BaseDBManager):

    def get_by_establishment(self, establishment_id):
        with connection.cursor() as c:
            c.execute('SELECT establishment_id, tag_name, user_name FROM "EstablishmentTags" WHERE establishment_id = %s;', [establishment_id])
            return [EstablishmentTag.from_db(d) for d in self.fetch_dicts(c)]


class Tag(object):

    db = TagDBManager()

    def __init__(self, name):
        self.name = name

    @classmethod
    def from_db(cls, db_dict):
        return cls(db_dict["name"])

class EstablishmentTag(object):

    db = EstablishmentTagDBManager()

    def __init__(self, establishment_id, tag_name, user_name):
        self.establishment_id = establishment_id
        self.tag_name = tag_name
        self.user_name = user_name

    @classmethod
    def from_db(cls, db_dict):
        return cls(db_dict["establishment_id"], db_dict["tag_name"], db_dict["user_name"])


