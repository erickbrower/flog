from __future__ import absolute_import 
from woodhouse.celery import celery
from api import APIRequest
from models import Application
from models import Log


@celery.task
def process_log_request(request_params):
    client_request = APIRequest(request_params)
    if not client_request.is_valid():
        return False
    instance = Application.objects(
            instance_key=client_request.params['_instance_key']
            ).only('private_key')
    if not instance: 
        return False
    if not client_request.authenticate(instance.private_key):
        return False
    log = Log(content=client_request.params, created=client_request.params['_timestamp'], application=instance)
    return log.save()
