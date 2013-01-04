from flask import Blueprint, request, abort, json, Response
from flog.models import Host, Log
from flog.api_request_authority import ApiRequestAuthority

api = Blueprint('api', __name__)

@api.route('/logs', methods=['GET'])
def list_logs():
    payload = dict(request.values.items())
    if '_api_key' not in payload:
        abort(400) #Nice try, amigo.
    the_host = Host.objects(api_key=payload['_api_key']).first()
    if not the_host:
        abort(400) #No host exists with that api_key
    try:
        if not ApiRequestAuthority.validate(payload, the_host.api_private_key):
            abort(400) #Couldn't validate signature
    except ValueError:
        abort(400)
    del payload['_api_key']
    del payload['_timestamp']
    del payload['_signature']
    results = Log.objects(host=the_host, **payload)
    #Format the result response
    res = [el._data for el in results]
    for thing in res:
        del thing['host']
        del thing[None]
    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if hasattr(obj, 'isoformat'):
                return obj.isoformat()
            else:
                return str(obj)
            return json.JSONEncoder.default(self, obj)
    return Response(json.dumps(res, cls=DateEncoder), status='200', mimetype='application/json')

@api.route('/logs', methods=['POST'])
def create_log():
    payload = dict(request.form.items())
    if not '_api_key' in payload:
        abort(400) #Nice try, amigo.
    the_host = Host.objects(api_key=payload['_api_key']).first()
    if not the_host:
        abort(400) #No host exists with that api_key
    try:
        if not ApiRequestAuthority.validate(payload, the_host.api_private_key):
            abort(400) #Couldn't validate signature
    except ValueError:
        abort(400)
    del payload['_signature']
    del payload['_api_key']
    del payload['_timestamp']
    log = Log(content=payload, host=the_host)
    js = {'status': 'success'} if log.save() else {'status': 'failure'}
    return Response(json.dumps(js), status='200', mimetype='application/json')

