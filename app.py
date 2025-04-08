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

    # ROUTES

    @app.route('/parking_lot', methods=['GET'])
    def display_parking_lot():
        floors = Floor.query.all()
        result = []
        for floor in floors:
            floor_data = {
                'floor_id': floor.floor_id,
                'floor_name': floor.floor_name,
                'rows': []
            }
            for row in floor.rows:
                row_data = {
                    'row_id': row.row_id,
                    'row_name': row.row_name,
                    'slots': []
                }
                for slot in row.slots:
                    slot_data = {
                        'slot_id': slot.slot_id,
                        'slot_name': slot.slot_name,
                        'status': slot.status,
                        'vehicle_reg_no': slot.vehicle_reg_no,
                        'ticket_id': slot.ticket_id
                    }
                    row_data['slots'].append(slot_data)
                floor_data['rows'].append(row_data)
            result.append(floor_data)
        return jsonify(result), 200

    @app.route('/park_car', methods=['POST'])
    def park_car():
        data = request.get_json()
        slot_id = data.get('slot_id')
        vehicle_reg_no = data.get('vehicle_reg_no')
        user_id = data.get('user_id')
        slot = Slot.query.get(slot_id)
        if not slot or slot.status == 0:
            return jsonify({'error': 'Slot is not available'}), 400
        ticket_id = f"TKT-{slot_id}-{int(datetime.utcnow().timestamp())}"
        slot.status = 0
        slot.vehicle_reg_no = vehicle_reg_no
        slot.ticket_id = ticket_id
        slot.user_id = user_id
        session = ParkingSession(
            ticket_id=ticket_id,
            slot_id=slot_id,
            vehicle_reg_no=vehicle_reg_no,
            user_id=user_id
        )
        db.session.add(session)
        db.session.commit()
        return jsonify({'message': 'Car parked successfully', 'ticket_id': ticket_id}), 201

    @app.route('/remove_car_by_ticket', methods=['DELETE'])
    def remove_car_by_ticket():
        data = request.get_json()
        ticket_id = data.get('ticket_id')
        slot = Slot.query.filter_by(ticket_id=ticket_id).first()
        if not slot:
            return jsonify({'error': 'Ticket not found'}), 404
        session = ParkingSession.query.get(ticket_id)
        if not session:
            return jsonify({'error': 'Parking session not found'}), 404
        slot.status = 1
        slot.vehicle_reg_no = None
        slot.ticket_id = None
        slot.user_id = None
        session.end_time = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': 'Car removed successfully'}), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([
            {
                'user_id': user.user_id,
                'user_name': user.user_name,
                'user_email': user.user_email,
                'user_phone_no': user.user_phone_no,
                'user_address': user.user_address
            } for user in users
        ]), 200

    @app.route('/users', methods=['POST'])
    def create_user():
        data = request.get_json()
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_password=data['user_password'],
            user_phone_no=data['user_phone_no'],
            user_address=data['user_address']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully', 'user_id': new_user.user_id}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'User with this email or phone already exists'}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        data = request.get_json()
        user.user_name = data.get('user_name', user.user_name)
        user.user_email = data.get('user_email', user.user_email)
        user.user_password = data.get('user_password', user.user_password)
        user.user_phone_no = data.get('user_phone_no', user.user_phone_no)
        user.user_address = data.get('user_address', user.user_address)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200

    return app
