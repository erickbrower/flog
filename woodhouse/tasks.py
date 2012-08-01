from __future__ import absolute_import 
from woodhouse.celery import celery
from api import APIRequest
from models import Application
from models import Log


@celery.task
def process_log_request(json_message):
    request = APIRequest(json_message)
    if not request.is_valid():
        return False
    instance = Application.objects(
            instance_key=request.params['_instance_key']
            ).only('private_key')
    if not instance: 
        return False
    if not request.authenticate(instance.private_key):
        return False
    log = Log(content=request.params, created=request.params['_timestamp'], application=instance)
    return log.save()
