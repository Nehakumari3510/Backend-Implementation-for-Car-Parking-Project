from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import urllib.parse

app = Flask(__name__)

username = "postgres" 
password = urllib.parse.quote_plus("postgres-admin") 
host = "localhost"
port = 5433 
database_name = "parking_db" 
password = urllib.parse.quote_plus("postgres-admin")
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models with relationships
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
    status = db.Column(db.Integer, default=1)  # 0 = Occupied, 1 = Free, 2 = Not in use
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

# Routes
@app.route('/parking_lot', methods=['GET'])
def display_parking_lot():
    try:
        floors = Floor.query.all()
        parking_lot = {}
        for floor in floors:
            rows = Row.query.filter_by(floor_id=floor.floor_id).all()
            rows_data = {}
            for row in rows:
                slots = Slot.query.filter_by(row_id=row.row_id).all()
                slots_data = []
                for slot in slots:
                    slots_data.append({
                        'slot_id': slot.slot_id,
                        'slot_name': slot.slot_name,
                        'status': slot.status,
                        'vehicle_reg_no': slot.vehicle_reg_no,
                        'ticket_id': slot.ticket_id,
                        'user_id': slot.user_id
                    })
                rows_data[row.row_name] = slots_data
            parking_lot[floor.floor_name] = rows_data
        return jsonify(parking_lot)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/park_car', methods=['POST'])
def park_car():
    try:
        data = request.get_json()
        vehicle_reg_no = data.get('vehicle_reg_no')

        if not vehicle_reg_no:
            return jsonify({"error": "Vehicle registration number is required."}), 400

        slot = Slot.query.filter_by(status=1).first()
        if not slot:
            return jsonify({"error": "No available slots."}), 400

        ticket_id = f"TICKET-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{slot.slot_id}"
        slot.status = 0
        slot.vehicle_reg_no = vehicle_reg_no
        slot.ticket_id = ticket_id
        db.session.commit()

        return jsonify({"message": "Car parked successfully.", "ticket_id": ticket_id}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error."}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/remove_car_by_ticket', methods=['DELETE'])
def remove_car_by_ticket():
    try:
        ticket_id = request.args.get('ticket_id')
        if not ticket_id:
            return jsonify({"error": "Ticket ID is required."}), 400

        slot = Slot.query.filter_by(ticket_id=ticket_id).first()
        if not slot:
            return jsonify({"error": "Ticket ID not found."}), 404

        slot.status = 1
        slot.vehicle_reg_no = None
        slot.ticket_id = None
        db.session.commit()

        return jsonify({"message": "Car removed successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# User APIs
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = []
        for user in users:
            users_data.append({
                'user_id': user.user_id,
                'user_name': user.user_name,
                'user_email': user.user_email,
                'user_password': user.user_password,
                'user_phone_no': user.user_phone_no,
                'user_address': user.user_address
            })
        return jsonify(users_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(
            user_name=data['user_name'],
            user_email=data['user_email'],
            user_password=data['user_password'],
            user_phone_no=data['user_phone_no'],
            user_address=data['user_address']
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully.", "user_id": new_user.user_id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error."}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.get_json()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found."}), 404

        user.user_name = data.get('user_name', user.user_name)
        user.user_email = data.get('user_email', user.user_email)
        user.user_password = data.get('user_password', user.user_password)
        user.user_phone_no = data.get('user_phone_no', user.user_phone_no)
        user.user_address = data.get('user_address', user.user_address)

        db.session.commit()
        return jsonify({"message": "User updated successfully."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
