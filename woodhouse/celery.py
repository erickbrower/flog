from __future__ import absolute_import
from celery import Celery

celery = Celery(broker='amqp://woodhouse:12345678@localhost:5672/dev_vhost', 
        include=['woodhouse.tasks'])

celery.conf.update(CELERY_TASK_RESULT_EXPIRES=3600)
