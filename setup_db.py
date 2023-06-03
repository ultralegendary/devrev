import sqlite3

DATABASE = 'dev_rev.db'
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row
def setup_database():

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT,
            email TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Flights (
            flight_id  TEXT PRIMARY KEY,
            poilt_name TEXT,
            source TEXT,
            destination TEXT,
            departure_time TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Seats (
        flight_id Integer,
        seat_id TEXT,
        price Integer,
        PRIMARY KEY (flight_id,seat_id),
        FOREIGN KEY (flight_id) REFERENCES flights (flight_id)
    )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id Integer,
        date_of_departure TEXT,
        passenger_name TEXT,
        flight_id INTEGER,
        seat_id TEXT,
        FOREIGN KEY (flight_id) REFERENCES flights (flight_id),
        FOREIGN KEY (user_id) REFERENCES user (user_id),
        FOREIGN KEY (seat_id) REFERENCES Seats (seat_id)
    )
        
    ''')
    conn.commit()

def populate():

    seat_classes = {
    'Economy': 30,
    'Business': 15,
    'First Class': 15,
    }
    cursor=conn.cursor()

    # Populate the Seats table for each flight and seat class
    flights = ['FL001', 'FL002', 'FL003']
    for flight_id in flights:
        for seat_class, seat_count in seat_classes.items():
            for seat_number in range(1, seat_count + 1):
                seat_id = f'{seat_class[0]}{seat_number:02d}'
                price = 0  # You can assign a price based on the seat class if needed

                print(flight_id, seat_id, seat_class, price)

    conn.commit()
    conn.close()
# setup_database()
populate()
# cursor=conn.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# rows = cursor.fetchall()
# print([row[0] for row in rows])
    