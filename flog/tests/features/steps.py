# -*- coding: utf-8 -*-
import os, sys, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import urllib
from flask import json
from lettuce import step, world
from flog import app
from flog.models import Host, Log
from flog.api_request_authority import ApiRequestAuthority

app.config['TESTING'] = True
client = app.test_client()
Host.drop_collection()

@step(u'Given I have some Hosts')
def given_i_have_some_hosts(step):
    Host.drop_collection()
    Log.drop_collection()
    for t_row in step.hashes:
        host = Host(**t_row)
        assert host.save()

@step(u'When I send requests to create new Log entries')
def when_i_send_requests_to_create_new_log_entries(step):
    world.responses = []
    for t_row in step.hashes:
        host = Host.objects(api_key=t_row['_api_key']).first()
        t_row['_timestamp'] = datetime.datetime.now().isoformat()
        ApiRequestAuthority.sign(t_row, host.api_private_key)
        response = client.post('/api/logs', data=t_row)
        world.responses.append(response)

@step(u'Then I should receive successful responses')
def then_i_should_receive_successful_responses(step):
    for response in world.responses:
        assert response._status_code == 200
        r = json.loads(response.data)
        assert 'status' in r
        assert r['status'] == 'success'

@step(u'And I have some Logs')
def and_i_have_some_logs(step):
    for t_row in step.hashes:
        host = Host.objects(api_key=t_row['host_api_key']).first()
        log = Log(**t_row)
        log.host = host
        log.save()

@step(u'When I send a request for all of \'([^\']*)\' Logs with \'([^\']*)\' = \'([^\']*)\'')
def when_i_send_a_request_for_all_of_group1_logs(step, host_key, field, value):
    host = Host.objects(api_key=host_key).first()
    req = { '_api_key': host_key, '_timestamp': datetime.datetime.now().isoformat() }
    req[field] = value
    ApiRequestAuthority.sign(req, host.api_private_key)
    world.response = client.get('/api/logs?' + urllib.urlencode(req))

@step(u'Then I should get the two Logs in the response')
def then_i_should_get_the_two_logs_in_the_response(step):
    assert world.response._status_code == 200
    r = json.loads(world.response.data)
    assert len(r) == 2
