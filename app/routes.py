from app import app
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_cors import CORS
from google.cloud import storage
from io import BytesIO

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


BUCKET_NAME = "gke-file-upload"


@app.route('/upload', methods=['POST'])
def upload_blob_from_memory():
    """Uploads a file to the bucket."""
    file = request.files.get('file')
    if file:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file)
        return jsonify({'url': blob.public_url})
    return jsonify({'error': 'A File is required'}), 400
