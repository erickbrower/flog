from flask import Blueprint, request, abort, json, Response
from flog.models import Log, KeyRing
from flog.key_master import KeyMaster

api = Blueprint('api', __name__)

@api.route('/logs', methods=['GET'])
def list_logs():
    payload = dict(request.values.items())
    kr = KeyRing.objects(public_key=payload[KeyMaster.PUB_KEY]).first()
    key = KeyMaster.check_keys(payload, kr.keys)
    if not key: 
        abort(400)
    log_data = KeyMaster.remove_keys(payload)
    logs = Log.objects(host=key.host, **log_data)
    return Response(Log.to_json(logs), status='200', mimetype='application/json')

@api.route('/logs', methods=['POST'])
def create_log():
    payload = dict(request.form.items())
    kr = KeyRing.objects(public_key=payload[KeyMaster.PUB_KEY]).first()
    key = KeyMaster.check_keys(payload, kr.keys)
    if not key:
        abort(400)
    log_data = KeyMaster.remove_keys(payload)
    log = Log(host=key.host, **log_data)
    r = {} 
    r['status'] = 'success' if log.save() else 'failure'
    return Response(json.dumps(r), status='200', mimetype='application/json')

