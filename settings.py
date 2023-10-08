import datetime

from flask import Flask
host = '127.0.0.1'


app = Flask(__name__)

app.config['SECRET_KEY'] = '__secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

UPLOAD_FOLDER = 'static/assets/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER1 = 'static/assets/images/clients'
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


user = 'postgres'
password = '12345'
db_name = 'mint'
