from __future__ import absolute_import
from flask import Flask
from flask import json
from flask import request
from flask import Response
from woodhouse.tasks import *

app = Flask('woodhouse')
app.config['MONGODB_DB'] = 'woodhouse_dev'
app.config['SECRET_KEY'] = '27dN3HfFgEOpEfdO'

@app.route('/log', methods=['POST'])
def api_log():
    if not request.headers['Content-Type'] == 'application/json':
        return False
    process_log_request.delay(request)
    response = Response(json.dumps({'received': 'ok'}), status=200, mimetype='application/json')
    return response

