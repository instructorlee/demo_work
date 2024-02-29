
from flask import Flask

UPLOAD_FOLDER = '/Users/leeloftiss/Desktop/cd/class_files/jan_24_python/my_pets/uploads'

app = Flask(__name__)
app.secret_key = "SomeSuperSecretComplexKey"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
