from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from db_password import my_password
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@127.0.0.1/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

