from django.db import connection
from common.models import BaseDBManager

class TagDBManager(BaseDBManager):
    pass

class EstablishmentTagDBManager(BaseDBManager):
    pass

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


