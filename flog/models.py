import datetime 
from flask import json
from flog import db
from flog.date_encoder import DateEncoder


class Host(db.Document):
    name = db.StringField(max_length=255, required=True)
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    description = db.StringField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['name', '-created'],
        'ordering': ['name']
    }


class Log(db.DynamicDocument):
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    host = db.ReferenceField(Host, dbref=False, required=True)

    @classmethod
    def to_json(cls, result_set):
        res = [el._data for el in result_set]
        for el in res:
            del el[None]
        return json.dumps(res, cls=DateEncoder)

    meta = {
        'indexes': ['-created', 'host']
    }


class Key(db.EmbeddedDocument):
    host = db.ReferenceField(Host, dbref=False, required=True)
    key = db.StringField(required=True)


class User(db.Document):
    email_address = db.StringField(required=True)
    password_hash = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {
        'indexes': ['email_address'],
        'ordering': ['email_address']
    }


class KeyRing(db.Document):
    public_key = db.StringField(unique=True)
    keys = db.ListField(db.EmbeddedDocumentField(Key))
    user = db.ReferenceField(User, dbref=False, required=True)

    meta = {
        'indexes': ['public_key']
    }
