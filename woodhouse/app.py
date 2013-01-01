from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)

app.config['MONGODB_DB'] = 'woodhouse_dev'
app.config['SECRET_KEY'] = 'd0ntp4nic'

db = MongoEngine(app)

@app.route('/applications', methods=['GET'])
def list_applications():
    pass

@app.route('/applications', methods=['POST'])
def create_applications():
    pass

@app.route('/applications/<int:application_id>', methods=['PUT'])
def update_applications(application_id):
    pass

@app.route('/applications/<int:application_id>', methods=['DELETE'])
def destroy_application(application_id):
    pass

@app.route('/logs', methods=['GET'])
def list_logs():
    pass

@app.route('/logs', methods=['POST'])
def create_log():
    pass


if __name__ == '__main__':
    app.run(debug=True)
