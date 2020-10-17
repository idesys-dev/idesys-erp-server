import os


from flask import Flask
from flask_cors import CORS
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface


from api.api_home import api_blueprint
from auth.views import auth_blueprint
from admin.admin_home import create_admin


try:
    SECRET_KEY = os.environ['FLASK_SECRET_KEY']
except KeyError:
    with open('flask.secret') as my_file:
        SECRET_KEY = my_file.read().strip()

try:
    MONGODB_URI = os.environ['MONGODB_URI']
except KeyError:
    with open('mongodb_uri.secret') as my_file:
        MONGODB_URI = my_file.read().strip()


# UPLOAD_FOLDER = 'data'

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint)
app.register_blueprint(auth_blueprint, url_prefix='/auth')

app.config['SECRET_KEY'] = SECRET_KEY
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 # allow 50 megabytes file

app.config['MONGODB_SETTINGS'] = {
    'host': MONGODB_URI
}
db = MongoEngine(app)
#app.session_interface = MongoEngineSessionInterface(db)

#create_admin(app)

@app.route('/')
def hello_world():
    return 'IdéSYS private API'


# Start the server on port 3001
if __name__ == "__main__":
    app.run(port=3001)
