from app import app
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS

import os

ALLOWED_EXTENSIONS = set(['xls', 'csv', 'png', 'jpeg', 'jpg', 'pdf'])
UPLOAD_FOLDER = "files"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000 * 1000  # 500 MB
app.config['CORS_HEADER'] = 'application/json'


def allowedFile(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/upload', methods=['POST'])
def fileUpload():
    file = request.files.getlist('files')
    filename = ""
    print(request.files, "....")
    for f in file:
        print(f.filename)
        filename = secure_filename(f.filename)
        print(allowedFile(filename))
        if allowedFile(filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return jsonify({'message': 'File type not allowed'}), 400
    return jsonify({"name": filename, "status": "success"})
