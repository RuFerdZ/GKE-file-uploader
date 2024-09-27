from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import secrets

app = Flask(__name__)

secret_key = secrets.token_hex(16)  # 32 characters (16 bytes)

# get from environment
DB_NAME = os.environ.get('DB_NAME', 'myappdb')
USER = os.environ.get('DB_USER', 'myuser')
PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')
HOST = os.environ.get('DB_HOST', '34.16.119.255')
PORT = '5432'

print(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')

# Configure the PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


# Create the tables if they don't exist
with app.app_context():
    db.create_all()

from app import routes
