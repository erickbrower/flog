from flask import Flask
from flask import json
from flask import request
from flask import Response
from flask.ext.mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_DB'] = 'woodhouse_dev'
app.config['SECRET_KEY'] = '27dN3HfFgEOpEfdO'
db = MongoEngine(app)

@app.route('/api', methods=['GET'])
def api_root():
    return json.dumps('Welcome')

@app.route('/api/log', methods=['GET'])
def api_log():
    #if not request.headers['Content-Type'] == 'application/json':
    #    return False
    entry = {'_timestamp': str(datetime.datetime.now()), '_instance_key': 'HORY_SHET_GOJIRA', 'entry': 'HORY SHET IT\'S GOJIRA', 'johnny': 'bravo' }
    h = hmac.new('12345678', entry['_instance_key'] + entry['_timestamp'], hashlib.sha256)
    entry['_signature'] = base64.b64encode(h.digest())
    process_log_request.delay(json.dumps(entry))
    response = Response(json.dumps({'received': 'ok'}), status=200, mimetype='application/json')
    return response
