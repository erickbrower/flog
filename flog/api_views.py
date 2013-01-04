from flask import Blueprint, request, abort, json, Response
from flog.models import Host, Log
from flog.api_request_authority import ApiRequestAuthority 

api = Blueprint('api', __name__)

def format_query_results(q_results):
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    res = [el._data for el in q_results]
    for el in res:
        del el['host']
        del el[None]
    return json.dumps(res, cls=DateEncoder)

def validate_payload(payload):
    if '_api_key' not in payload:
        abort(400) #Nice try, amigo.
    host = Host.objects(api_key=payload['_api_key']).first()
    if not host:
        abort(400) #No host exists with that api_key
    try:
        if not ApiRequestAuthority.validate(payload, host.api_private_key):
            abort(400) #Couldn't validate signature
    except ValueError:
        abort(400)
    return host

def clean_sig_data(payload):
    del payload['_api_key']
    del payload['_timestamp']
    del payload['_signature']

@api.route('/logs', methods=['GET'])
def list_logs():
    payload = dict(request.values.items())
    host = validate_payload(payload)
    clean_sig_data(payload)
    results = Log.objects(host=host, **payload)
    r_content = format_query_results(results)
    return Response(r_content, status='200', mimetype='application/json')

@api.route('/logs', methods=['POST'])
def create_log():
    payload = dict(request.form.items())
    host = validate_payload(payload)
    clean_sig_data(payload)
    log = Log(**payload)
    log.host = host
    js = {'status': 'success'} if log.save() else {'status': 'failure'}
    return Response(json.dumps(js), status='200', mimetype='application/json')

