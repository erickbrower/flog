from __future__ import absolute_import
from celery import Celery
from woodhouse.models import Application, Log
from woodhouse.api_request import APIRequest

celery = Celery(broker='amqp://woodhouse:12345678@localhost:5672/dev_vhost', 
        include=['woodhouse.tasks'])
celery.conf.update(CELERY_TASK_RESULT_EXPIRES=3600)

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


