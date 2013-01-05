import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import urllib
from flask import json
from lettuce import step, world
from flog import app
from flog.models import Host, Log, KeyRing, Key, User
from flog.key_master import KeyMaster 
from pprint import pprint

app.config['TESTING'] = True
client = app.test_client()

@step(u'Given I have a User account')
def given_i_have_a_user_account(step):
    User.drop_collection()
    for tr in step.hashes:
        user = User(**tr)
        user.save()

@step(u'And I have a Host')
def and_i_have_a_host(step):
    Host.drop_collection()
    for tr in step.hashes:
        host = Host(**tr)
        assert host.save()

@step(u'And my User KeyRing has a Key to the Host')
def and_my_user_keyring_has_a_key_to_the_host(step):
    KeyRing.drop_collection()
    user = User.objects.first()
    host = Host.objects.first()
    for tr in step.hashes:
        world.public_key = tr['public_key']
        world.private_key = tr['private_key']
        kr = KeyRing(public_key=tr['public_key'])
        kr.keys.append(Key(host=host, key=world.private_key))
        kr.save()
        user.key_ring = kr
        user.save()

@step(u'When I send requests to create new Log entries')
def when_i_send_requests_to_create_new_log_entries(step):
    Log.drop_collection()
    world.responses = []
    for tr in step.hashes:
        tr[KeyMaster.TIME_KEY] = time.time()
        payload = KeyMaster.sign(tr, world.private_key)
        tr[KeyMaster.SIG_KEY] = payload['_signature']
        response = client.post('/api/logs', data=payload)
        world.responses.append(response)
        pprint(response)

@step(u'Then I should receive successful responses')
def then_i_should_receive_successful_responses(step):
    for response in world.responses:
        assert response._status_code == 200
        r = json.loads(response.data)
        assert 'status' in r
        assert r['status'] == 'success'

@step(u'And I have some Logs')
def and_i_have_some_logs(step):
    for tr in step.hashes:
        host = Host.objects.first()
        log = Log(**tr)
        log.host = host
        log.save()

@step(u'When I send a request for all of the Host Logs with \'([^\']*)\' = \'([^\']*)\'')
def when_i_send_a_request_for_all_of_the_host_logs_with_group1_group2(step, field, value):
    payload = { field: value }
    payload[KeyMaster.PUB_KEY] = world.public_key
    payload[KeyMaster.TIME_KEY] = time.time()
    signed = KeyMaster.sign(payload, world.private_key)
    response = client.get('/api/logs?' + urllib.urlencode(signed))
    world.response = response

@step(u'Then I should get the two Logs in the response')
def then_i_should_get_the_two_logs_in_the_response(step):
    assert world.response._status_code == 200
    r = json.loads(world.response.data)
    assert len(r) == 2

