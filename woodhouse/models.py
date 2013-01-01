import datetime
from woodhouse.app import db


class Application(db.Document):
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


class Log(db.Document):
    content = db.DictField()
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    application = db.ReferenceField(Application, dbref=False, required=True)

    meta = {
        'max_size': 2000000000,
        'indexes': ['-created', 'application']
    }
