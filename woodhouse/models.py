from __future__ import absolute_import
from woodhouse.__init__ import app
from flask.ext.mongoengine import MongoEngine
import datetime

db = MongoEngine(app)

class Application(db.Document):
    name = db.StringField(max_length=255)
    instance = db.StringField(max_length=255)
    api_key = db.StringField(max_length=255, unique=True)
    api_private_key = db.StringField()
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    description = db.StringField()
    ip_addresses = db.ListField(db.StringField())

    meta = {
        'allow_inheritance': True,
        'indexes': ['name', '-created'],
        'ordering': ['name']
    }


class Log(db.Document):
    content = db.DictField()
    created = db.DateTimeField(default=datetime.datetime.now, required=True)
    application = db.ReferenceField('Application')

    meta = {
        'max_size': 2000000000,
        'indexes': ['-created', 'application']
    }

