import datetime 
from flog import db 


class Host(db.Document):
    name = db.StringField(max_length=255, required=True)
    instance = db.StringField(max_length=255)
    api_key = db.StringField(max_length=255, unique=True, required=True)
    api_private_key = db.StringField(required=True)
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

    meta = {
        'indexes': ['-created', 'host']
    }


class User(db.Document):
    email_address = db.StringField(required=True)
    password_hash = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.datetime.now, required=True)

    meta = {
        'indexes': ['email_address'],
        'ordering': ['email_address']
    }
