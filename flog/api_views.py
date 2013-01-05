from flask import Blueprint, request, abort, json, Response
from flog.models import Log, Host
from flog.lib.notary import Notary

api = Blueprint('api', __name__)

@api.route('/logs', methods=['GET'])
def list_logs():
    payload = dict(request.values.items())
    host = Host.objects(api_key=payload[Notary.public_key]).first()
    if not host or not Notary.validate(payload, host.api_private_key):
        abort(400)
    log_data = Notary.clean(payload)
    logs = Log.objects(host=host.id, **log_data)
    r_content = Log.to_json(logs)
    return Response(r_content, status='200', mimetype='application/json')

@api.route('/logs', methods=['POST'])
def create_log():
    payload = dict(request.form.items())
    host = Host.objects(api_key=payload[Notary.public_key]).first()
    if not host or not Notary.validate(payload, host.api_private_key):
        abort(400)
    if not host:
        abort(400)
    log_data = Notary.clean(payload)
    log = Log(**log_data)
    log.host = host
    js = {'status': 'success'} if log.save() else {'status': 'failure'}
    return Response(json.dumps(js), status='200', mimetype='application/json')

