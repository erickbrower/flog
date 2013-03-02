import os, sys, time, urllib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from lettuce import step, world
from flask import json
from flog import app
from flog.models import db
from flog.key_master import KeyMaster 

app.config['TESTING'] = True
client = app.test_client()

@step(u'Given I have a Node')
def given_i_have_a_node(step):
    db.drop_collection('nodes')
    world.nodes = []
    for tr in step.hashes:
        node = db.nodes.Node()
        for key, value in tr.items():
            node[key] = value
        node.save()
        world.nodes.append(node)

@step(u'And I have a Stream')
def and_i_have_a_stream(step):
    db.drop_collection('streams')
    world.streams = []
    for tr in step.hashes:
        stream = db.streams.Stream()
        for key, value in tr.items():
            stream[key] = value
        stream.node = world.nodes[0]
        stream.save()
        world.streams.append(stream)
            
@step(u'When I send requests to add new Log entries to the Stream')
def when_i_send_requests_to_add_new_log_entries_to_the_stream(step):
    world.responses = []
    for tr in step.hashes:
        tr[KeyMaster.TIME_KEY] = time.time()
        payload = KeyMaster.sign(tr, world.streams[0]['private_key'])
        tr[KeyMaster.SIG_KEY] = payload['_signature']
        response = client.post('/api/logs', data=payload)
        world.responses.append(response)

@step(u'Then I should receive successful responses')
def then_i_should_receive_successful_responses(step):
    for resp in world.responses:
        assert resp._status_code == 200
        r = json.loads(resp.data)
        assert 'status' in r
        assert r['status'] == 'success'

@step(u'And I have some Logs')
def and_i_have_some_logs(step):
    world.logs = []
    stream = world.streams[0]
    db.drop_collection(stream['log_collection'])
    for tr in step.hashes:
        log = db[stream['log_collection']].Log()
        for key, value in tr.items():
            log[key] = value
        log.save()
        world.logs.append(log)

@step(u'When I send a request for all of the Stream Logs with \'([^\']*)\' = \'([^\']*)\'')
def when_i_send_a_request_for_all_of_the_stream_logs_with_group1_group2(step, field, value):
    payload = {field: value}
    payload[KeyMaster.PUB_KEY] = world.streams[0]['public_key']
    payload[KeyMaster.TIME_KEY] = time.time()
    signed = KeyMaster.sign(payload, world.streams[0]['private_key'])
    response = client.get('/api/logs?' + urllib.urlencode(signed))
    world.response = response

@step(u'Then I should get the two Logs in the response')
def then_i_should_get_the_two_logs_in_the_response(step):
    js = json.loads(world.response.data)
    assert len(js) == 2
    db.drop_collection(world.streams[0]['log_collection'])
