import datetime

from flask import Flask

GENERAL_NAME_LINK = 'http://127.0.0.1:5000'


app = Flask(__name__)

app.config['SECRET_KEY'] = '__secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

app.config['UPLOAD_FOLDER1'] = 'static/assets/images/clients'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

# app.config['UPLOADED_PHOTOS_DEST'] = 'static/assets/images/clients'
#
# photos = UploadSet('photos', IMAGES)
# configure_uploads(app, photos)
# # максимальный размер файла, по умолчанию 16MB
# patch_request_class(app)
