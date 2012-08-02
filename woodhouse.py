from __future__ import absolute_import
from celery import Celery
from flask import Flask
from flask import json
from flask import request
from flask import Response
from flask.ext.mongoengine import MongoEngine
import datetime
import urllib
import hmac
import hashlib
import base64

app = Flask('woodhouse')
app.config['MONGODB_DB'] = 'woodhouse_dev'
app.config['SECRET_KEY'] = '27dN3HfFgEOpEfdO'
db = MongoEngine(app)

celery = Celery(broker='amqp://woodhouse:12345678@localhost:5672/dev_vhost', 
        include=['woodhouse.tasks'])

celery.conf.update(CELERY_TASK_RESULT_EXPIRES=3600)

@app.route('/log', methods=['POST'])
def api_log():
    if not request.headers['Content-Type'] == 'application/json':
        return False
    process_log_request.delay(request)
    response = Response(json.dumps({'received': 'ok'}), status=200, mimetype='application/json')
    return response

@celery.task
def process_log_request(request):
    if not request.json: 
        return False
    instance = Application.objects(
            instance_key=request.json['_instance_key']
            ).only('private_key')
    if not instance: 
        return False
    api_request = APIRequest(request.json)
    if not api_request.authenticate(instance.private_key):
        return False
    del api_request.params['_signature']
    log = Log(content=api_request.params, created=api_request.params['_timestamp'], application=instance)
    return log.save()


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


class InvalidRequestParamsError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

   
class APIRequest(object): 
    """ Provides methods for signing and authenticating RESTful API requests.

    Create a new API Request like this:
   
        my_request = APIRequest()
        my_request.params['message'] = 'HORY SHET IT\'S GOJIRA'
        request.sign('MyPrivateKey123')
       
    """
    def __init__(self, params=None):
        self.params = {} 
        if params and isinstance(params, dict):
            self.params = params 

    def __str__(self):
        return self._encode_params(self.params) 

    def sign(self, private_key):
        """Generates an encoded url string that contains an encrypted signature. 
        
        This hash is then set to a property on the object
        (self.params['_signature']) and returned. 
        
        Args:
            private_key: The private key used to create the request signature.

        Returns: 
            An encrypted hash of type string. 

        Raises:
            InvalidRequestParamsError: Either the _instance_key or the 
                _timestamp request params are missing.
        """
        if not self._can_be_signed():
            raise InvalidRequestParamsError(('The request params must contain' 
                ' _instance_key and _timestamp.'))
        self.params['_signature'] = self._create_signature(private_key)
        return self._encode_params(self.params)
    
    def authenticate(self, private_key):
        """Determines if the request is properly signed with the private key.

        An encrypted hash is generated using the request params and the private
        key. If the generated hash matches the request signature 
        (self.params['_signature']) then the request is authentic. 

        Args:
            private_key: The private key used to check the request signature.

        Returns:
            True if the generated hash matches the request signature, False
            if not.

        Raises:
            InvalidRequestParamsError: The _signature request param is missing.
        """
        if not self._is_signed():
            raise InvalidRequestParamsError('The request has not been signed.')
        return self._create_signature(private_key) == self.params['_signature'] 
    
    def is_valid(self):
        return self._can_be_signed()

    def _create_signature(self, private_key):
        """Creates an encrypted hash from the request params and private key.
        
        The public key is created by sorting the current request params, 
        without _signature, in alphabetical order and url encoding them. The 
        public and private keys are then used to generate a hash.

        Args:
            private_key: The private key used to create the encrypted hash.

        Returns:
            An encrypted hash of type string.
        """
        params_copy = self.params.copy()
        if '_signature' in params_copy:
            del params_copy['_signature']
        encoded_params = self._encode_params(params_copy)
        signature_digest = hmac.new(private_key, encoded_params, 
                digestmod=hashlib.sha256).digest()
        return base64.b64encode(signature_digest).decode()

    def _encode_params(self, params):
        items = params.items()
        items.sort()
        return urllib.urlencode(dict(items))

    def _is_signed(self):
        return '_signature' in self.params

    def _can_be_signed(self):
        return '_instance_key' in self.params and '_timestamp' in self.params

app.run(debug=True)
