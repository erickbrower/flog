# -*- coding: utf-8 -*-
import os, sys, time, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import urllib
from flask import json
from lettuce import step
from woodhouse import app
from woodhouse.models import Host, Log
from woodhouse.api_request_authority import ApiRequestAuthority
from pprint import pprint


app.config['TESTING'] = True
client = app.test_client()
Host.drop_collection()
Log.drop_collection()

@step(u'Given I have some valid Hosts')
def given_i_have_some_valid_hosts(step):
    for h_data in step.hashes:
        host = Host(**h_data)
        assert host.save()

@step(u'When I send requests to create new Log entries')
def when_i_send_requests_to_create_new_log_entries(step):
    for r_data in step.hashes:
        host = Host.objects(api_key=r_data['_api_key']).first()
        r_data['_timestamp'] = time.time()
        ApiRequestAuthority.sign(r_data, host.api_private_key)
        response = client.post('/logs', data=r_data)
        r = json.loads(response.data)
        assert 'status' in r
        assert r['status'] == 'success'

@step(u'Then I should be able to query for the Logs')
def then_i_should_be_able_to_query_for_the_logs(step):
    for q_data in step.hashes:
        host = Host.objects(api_key=q_data['_api_key']).first()
        q_data['_timestamp'] = datetime.datetime.now().isoformat()
        ApiRequestAuthority.sign(q_data, host.api_private_key)
        response = client.get('/logs?' + urllib.urlencode(q_data))
        assert response._status_code != 400
