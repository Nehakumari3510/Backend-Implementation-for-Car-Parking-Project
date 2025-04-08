from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import urllib.parse

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        username = "postgres" 
        password = urllib.parse.quote_plus("postgres-admin") 
        host = "localhost"
        port = 5433 
        database_name = "parking_db"
        app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # MODELS
    class Floor(db.Model):
        __tablename__ = 'floors'
        floor_id = db.Column(db.Integer, primary_key=True)
        floor_name = db.Column(db.String(50))
        rows = db.relationship('Row', backref='floor', lazy=True)

    class Row(db.Model):
        __tablename__ = 'rows'
        row_id = db.Column(db.Integer, primary_key=True)
        floor_id = db.Column(db.Integer, db.ForeignKey('floors.floor_id'))
        row_name = db.Column(db.String(50))
        slots = db.relationship('Slot', backref='row', lazy=True)

    class Slot(db.Model):
        __tablename__ = 'slots'
        slot_id = db.Column(db.Integer, primary_key=True)
        row_id = db.Column(db.Integer, db.ForeignKey('rows.row_id'))
        slot_name = db.Column(db.String(50))
        status = db.Column(db.Integer, default=1)
        vehicle_reg_no = db.Column(db.String(20), nullable=True)
        ticket_id = db.Column(db.String(20), nullable=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    class User(db.Model):
        __tablename__ = 'users'
        user_id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String(100))
        user_email = db.Column(db.String(100))
        user_password = db.Column(db.String(50))
        user_phone_no = db.Column(db.String(20))
        user_address = db.Column(db.String(100))

    class ParkingSession(db.Model):
        __tablename__ = 'parkingsessions'
        ticket_id = db.Column(db.String(20), primary_key=True)
        slot_id = db.Column(db.Integer, db.ForeignKey('slots.slot_id'))
        vehicle_reg_no = db.Column(db.String(20))
        start_time = db.Column(db.DateTime, default=datetime.utcnow)
        end_time = db.Column(db.DateTime, nullable=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # ROUTES (same as you already have)
    @app.route('/parking_lot', methods=['GET'])
    def display_parking_lot():
        ...

    @app.route('/park_car', methods=['POST'])
    def park_car():
        ...

    @app.route('/remove_car_by_ticket', methods=['DELETE'])
    def remove_car_by_ticket():
        ...

    @app.route('/users', methods=['GET'])
    def get_users():
        ...

    @app.route('/users', methods=['POST'])
    def create_user():
        ...

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        ...

    return app
