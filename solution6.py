from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import urllib.parse

app = Flask(__name__)

# URL encode the password to handle special characters
password = urllib.parse.quote_plus("Khalid@1704")
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:{password}@localhost/parking_db"
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
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(50))
    address = db.Column(db.String(255))
    registration_no = db.Column(db.String(20))

class Reservation(db.Model):
    __tablename__ = 'reservations'
    reservation_id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.slot_id'))
    hour = db.Column(db.Integer)
    reserved = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

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

# Additional routes and corrections can be added similarly.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



