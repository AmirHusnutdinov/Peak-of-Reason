import datetime

from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY'] = '__secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

app.config['UPLOAD_FOLDER1'] = 'static/assets/images/clients'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

