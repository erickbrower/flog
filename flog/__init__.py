from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask('flog')
app.config['MONGODB_DB'] = 'flog_dev'
app.config['SECRET_KEY'] = 'd0ntp4nic'

db = MongoEngine(app)

from flog.api_views import api
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
