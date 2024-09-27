from flask import jsonify, request, render_template, url_for, redirect, flash
from google.cloud import storage

from werkzeug.security import generate_password_hash
from app import app, db, User

BUCKET_NAME = "gke-file-upload"


# @app.route('/')
# @app.route('/index')
# def index():
#     return "Hello, World!"


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


# Route to display the Add User form and process the user submission
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            return render_template('add_user.html', error='Please fill all fields')

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('add_user.html', error='Email already exists')

        # Add new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Flash success message
        # flash('User added successfully!', 'success')
        return redirect(url_for('get_user', user_id=new_user.id))

    return render_template('add_user.html')


# Route to display user information by ID
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return render_template('user.html', error='User not found')

    return render_template('user.html', user=user)

# @app.route('/add-user', methods=['POST'])
# def register_user():
#     data = request.get_json()
#     if not data or not all(k in data for k in ("name", "email", "password")):
#         return jsonify({'error': 'Missing fields'}), 400
#
#     new_user = User(name=data['name'], email=data['email'], password=generate_password_hash(data['password']))
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User Added successfully'}), 201


# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = User.query.get(user_id)
#     if user is None:
#         return jsonify({'error': 'User not found'}), 404
#
#     return jsonify({
#         'id': user.id,
#         'name': user.name,
#         'email': user.email,
#     }), 200
