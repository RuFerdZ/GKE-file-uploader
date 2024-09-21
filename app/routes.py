from flask import jsonify, request
from google.cloud import storage

from app import app

BUCKET_NAME = "gke-file-upload"


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


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

