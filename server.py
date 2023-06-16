from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    email = request.form.get('email')
    password = request.form.get('password')

    # Check user credentials in the SQLite database
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM admin WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        response = {'status': 'success', 'message': 'Login successful','name':user[0]}
    else:
        response = {'status': 'failure', 'message': 'Invalid email or password'}

    return jsonify(response)

@app.route('/userlogin', methods=['POST'])
def userlogin():
    email = request.form.get('email')
    password = request.form.get('password')
    
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM user WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        response = {'status': 'success', 'message': 'Login successful','name':user[0]}
    else:
        response = {'status': 'failure', 'message': 'Invalid email or password'}

    return jsonify(response)

@app.route('/bookings', methods=['GET'])
def get_bookings():
    date = request.args.get('date')
    flight_id = request.args.get('flight_id')

    # Retrieve bookings for the flight and date from the SQLite database
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Bookings.seat_id, Bookings.passenger_name, Seats.seat_class
        FROM Bookings
        INNER JOIN Seats ON Bookings.seat_id = Seats.seat_id and bookings.flight_id=seats.flight_id
        WHERE Bookings.date_of_departure = ? AND Bookings.flight_id = ?
    ''', (date, flight_id))
    bookings = cursor.fetchall()
    conn.close()

    if bookings:
        response = {
            'status': 'success',
            'message': 'Bookings retrieved successfully',
            'bookings': [{
                'seat_id': booking[0],
                'passenger_name': booking[1],
                'seat_type': booking[2]
            } for booking in bookings]
        }
    else:
        response = {
            'status': 'failure',
            'message': 'No bookings found for the flight on the specified date',
            'bookings': []
        }

    return jsonify(response)

@app.route('/seats', methods=['GET'])
def get_available_seats():
    date = request.args.get('date')
    flight_id = request.args.get('flight_id')

    # Retrieve available seats for the flight and date from the SQLite database
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Seats.seat_id, Seats.price,Seats.seat_class
        FROM seats
        Where flight_id = ? and seat_id not in (select seat_id from bookings where flight_id = ? and bookings.date_of_departure = ? )''', (flight_id,flight_id,date))
    available_seats = cursor.fetchall()
    conn.close()
    print('''SELECT Seats.seat_id, Seats.price,Seats.seat_class FROM Seats        Where flight_id = '{}' and seat_id not in (select seat_id from bookings where flight_id = '{}' and bookings.date_of_departure = '{}' )'''.format(flight_id,flight_id,date))

    if available_seats:
        response = {
            'status': 'success',
            'message': 'Available seats retrieved successfully',
            'seats': [{
                'seat_id': seat[0],
                'price': seat[1],
                'class': seat[2]
            } for seat in available_seats]
        }
    else:
        response = {
            'status': 'failure',
            'message': 'No available seats found for the flight on the specified date',
            'seats': []
        }

    return jsonify(response)

@app.route('/book', methods=['POST'])
def book_seats():
    user_id = request.form.get('user_id')
    date_of_departure = request.form.get('date_of_departure')
    flight_id = request.form.get('flight_id')
    seat_ids = request.form.getlist('seat_id')
    passenger_names = request.form.getlist('passenger_name')

    # Validate that the number of seat IDs and passenger names match
    if len(seat_ids) != len(passenger_names):
        response = {
            'status': 'failure',
            'message': 'The number of seat IDs and passenger names must be the same',
            'booking_ids': []
        }
        return jsonify(response), 400

    # Perform the bookings by inserting into the Bookings table
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    
    booking_ids = []
    for seat_id, passenger_name in zip(seat_ids, passenger_names):
        cursor.execute('''
            INSERT INTO Bookings (user_id, date_of_departure, passenger_name, flight_id, seat_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, date_of_departure, passenger_name, flight_id, seat_id))
        booking_ids.append(cursor.lastrowid)

    conn.commit()
    conn.close()

    response = {
        'status': 'success',
        'message': 'Seats booked successfully',
        'booking_ids': booking_ids
    }

    return jsonify(response)

@app.route('/userbookings', methods=['GET'])
def get_user_bookings():
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    
    user_id = request.args.get('user_id')
    
    # Retrieve bookings for the specified user ID and join with Flights table
    cursor.execute('''
        SELECT Bookings.booking_id, Bookings.user_id, Bookings.date_of_departure,
               Bookings.passenger_name, Flights.source, Flights.destination
        FROM Bookings
        JOIN Flights ON Bookings.flight_id = Flights.flight_id
        WHERE Bookings.user_id = ?
    ''', (user_id,))
    print(user_id)
    bookings = []
    for row in cursor.fetchall():
        booking = {
            'booking_id': row[0],
            'user_id': row[1],
            'date_of_departure': row[2],
            'passenger_name': row[3],
            'source': row[4],
            'destination': row[5]
        }
        bookings.append(booking)

    conn.close()

    response = {
        'status': 'success',
        'bookings': bookings
    }

    return jsonify(response)

@app.route('/add_flight', methods=['POST'])
def add_flight():
    flight_id = request.form.get('flight_id')
    pilot_name = request.form.get('pilot_name')
    source = request.form.get('source')
    destination = request.form.get('destination')
    departure_time = request.form.get('departure_time')

    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()

    # Check if the flight ID already exists
    cursor.execute('SELECT * FROM Flights WHERE flight_id = ?', (flight_id,))
    existing_flight = cursor.fetchone()
    if existing_flight:
        response = {
            'status': 'failure',
            'message': 'Flight ID already exists'
        }
        return jsonify(response), 400

    # Insert the new flight into the Flights table
    cursor.execute('''
        INSERT INTO Flights (flight_id, poilt_name, source, destination, departure_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (flight_id, pilot_name, source, destination, departure_time))

    conn.commit()
    conn.close()

    response = {
        'status': 'success',
        'message': 'Flight added successfully'
    }

    return jsonify(response)


# API endpoint for removing a flight
@app.route('/remove_flights', methods=['DELETE'])
def remove_flight():
    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()
    flight_id=request.args.get("flight_id")

    # Check if the flight ID exists
    cursor.execute('SELECT * FROM Flights WHERE flight_id = ?', (flight_id,))
    existing_flight = cursor.fetchone()
    if not existing_flight:
        response = {
            'status': 'failure',
            'message': 'Flight ID does not exist'
        }
        return jsonify(response), 400

    # Remove the flight from the Flights table
    cursor.execute('DELETE FROM Flights WHERE flight_id = ?', (flight_id,))

    conn.commit()
    conn.close()

    response = {
        'status': 'success',
        'message': 'Flight removed successfully'
    }

    return jsonify(response)

@app.route('/register', methods=['POST'])
def register_user():
    name = request.form.get('name')
    password = request.form.get('password')
    email = request.form.get('email')

    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()

    # Check if the email is already registered
    cursor.execute('SELECT * FROM User WHERE email = ?', (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        response = {
            'status': 'failure',
            'message': 'Email is already registered'
        }
        return jsonify(response), 400

    # Insert the new user into the User table
    cursor.execute('''
        INSERT INTO User (name, password, email)
        VALUES (?, ?, ?)
    ''', (name, password, email))

    conn.commit()
    conn.close()

    response = {
        'status': 'success',
        'message': 'User registered successfully'
    }

    return jsonify(response)

@app.route('/booked_flights', methods=['GET'])
def get_booked_flights():

    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()

    # Retrieve the booked flights for the given user_id
    cursor.execute('''
        SELECT DISTINCT flight_id
        FROM Bookings
    ''')
    booked_flights = cursor.fetchall()

    conn.close()

    response = {
        'booked_flights': booked_flights
    }

    return jsonify(response)

@app.route('/booked_dates', methods=['GET'])
def get_booked_dates():
    flight_id = request.args.get('flight_id')

    conn = sqlite3.connect('dev_rev.db')
    cursor = conn.cursor()

    # Retrieve the booked dates for the given user_id and flight_id
    cursor.execute('''
        SELECT DISTINCT Bookings.date_of_departure
        FROM Bookings
        WHERE Bookings.flight_id = ?
    ''', (flight_id,))
    booked_dates = cursor.fetchall()

    conn.close()

    response = {
        'booked_dates': booked_dates
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run()
