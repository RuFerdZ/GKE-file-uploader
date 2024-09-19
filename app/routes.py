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


# @app.route('/upload-local', methods=['POST'])
# def fileUpload():
#     file = request.files.getlist('files')
#     filename = ""
#     print(request.files, "....")
#     for f in file:
#         print(f.filename)
#         filename = secure_filename(f.filename)
#         print(allowedFile(filename))
#         if allowedFile(filename):
#             f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         else:
#             return jsonify({'message': 'File type not allowed'}), 400
#     return jsonify({"name": filename, "status": "success"})

BUCKET_NAME = "gke-file-upload"


def gcs_upload_image(filename: str):
    storage_client: storage.Client = storage.Client()
    bucket: storage.Bucket = storage_client.bucket(BUCKET_NAME)
    bucket.iam_configuration.uniform_bucket_level_access_enabled = False
    bucket.patch()
    blob: storage.Blob = bucket.blob(filename.split("/")[-1])
    blob.upload_from_filename(filename)
    blob.make_public()
    public_url: str = blob.public_url
    print(f"Image uploaded to {public_url}")
    os.remove(filename)
    return public_url


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files.get('files')
    if not file:
        return jsonify({'error': 'A File is required'}), 400,
    tmp_file = f'files/{file.filename}'
    file.save(tmp_file)
    url = gcs_upload_image(tmp_file)
    # os.remove(tmp_file)
    return jsonify({'url': url})
