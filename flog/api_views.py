from flask import Blueprint, request, abort, json, Response
from flog.models import db
from flog.key_master import KeyMaster

api = Blueprint('api', __name__)

@api.route('/logs', methods=['GET', 'POST'])
def manage_logs():
    payload = dict(request.values.items())
    if '_public_key' not in payload:
        abort(400)
    stream = db.Stream.find_one({'public_key': payload['_public_key']})
    if not KeyMaster.check(payload, stream['private_key']):
        abort(400)
    log_data = KeyMaster.remove_keys(payload)
    if request.method == 'GET':
        resp = u'[' + ', '.join([log.to_json() for log in 
            db[stream['log_collection']].Log.find(log_data)]) + ']'
    elif request.method == 'POST':
        log = db[stream['log_collection']].Log()
        for key, value in log_data.items():
            log[key] = value
        try:
            log.save()
            resp = json.dumps({'status': 'success'})
        except:
            resp = json.dumps({'status': 'error'})
    else:
        abort(400)
    return Response(resp, status='200', mimetype='application/json')
