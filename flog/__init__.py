from flask import Flask

app = Flask('flog')

from flog.api_views import api
app.register_blueprint(api, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
