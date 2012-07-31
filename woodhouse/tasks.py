from celery import Celery
import json, urllib, datetime, hmac, hashlib, base64
from models import Application, Log

celery = Celery('tasks', broker='amqp://woodhouse:12345678@localhost:5672/dev_vhost')

def _validate_request(json_string):
    params = json.loads(json_string)
    #validate api_public_key, timestamp, type, and signature fields exist
    if not params or len(params) <= 4:
        return False
    if not '_api_key' in params or not '_timestamp' in params or not '_signature' in params:
        return False
    apps = Application.objects(api_key=params['_api_key']).only('api_private_key')
    app = apps.first()
    if not app:
        return False
    digest = hmac.new(app.api_private_key, str(params['_api_key'] + params['_timestamp']), digestmod=hashlib.sha256).digest()
    #Compare the two hashes
    if base64.b64encode(digest).decode() != params['_signature']:
        return False
    del params['_signature']
    del params['_api_key']
    return params

@celery.task(name='woodhouse.tasks.process_log_request')
def process_log_request(json_string):
    params = _validate_request(json_string)
    if not params:
        return False
    client_timestamp = params['_timestamp']
    del params['_timestamp']
    print 'HERE!'
    log = Log(content=params, created=client_timestamp, application=app)
    return log.save()
