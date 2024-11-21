
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DB_PATH = 'cars.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        make TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        price REAL NOT NULL
    )''')
    conn.commit()
    conn.close()

def populate_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executemany('''INSERT INTO cars (make, model, year, price)
                          VALUES (?, ?, ?, ?)''', [
        ('Toyota', 'Camry', 2020, 24000),
        ('Honda', 'Civic', 2019, 20000),
        ('Ford', 'Mustang', 2021, 30000),
        ('Chevrolet', 'Impala', 2018, 22000),
        ('Tesla', 'Model S', 2022, 85000),
        # Add 45 more entries with realistic data
        ('BMW', 'X5', 2020, 60000),
        ('Audi', 'A4', 2018, 35000),
        ('Hyundai', 'Elantra', 2019, 19000),
        ('Kia', 'Sorento', 2021, 28000),
        ('Nissan', 'Altima', 2020, 24000)
    ])
    conn.commit()
    conn.close()

@app.route('/cars', methods=['GET', 'POST'])
def cars():
    if request.method == 'GET':
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cars")
        rows = cursor.fetchall()
        conn.close()
        return jsonify(rows)
    elif request.method == 'POST':
        data = request.json
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO cars (make, model, year, price)
                          VALUES (?, ?, ?, ?)''',
                       (data['make'], data['model'], data['year'], data['price']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Car added successfully!'})

@app.route('/cars/<int:car_id>', methods=['GET', 'PUT', 'DELETE'])
def car_detail(car_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM cars WHERE id = ?", (car_id,))
        car = cursor.fetchone()
        conn.close()
        return jsonify(car)
    elif request.method == 'PUT':
        data = request.json
        cursor.execute('''UPDATE cars SET make = ?, model = ?, year = ?, price = ?
                          WHERE id = ?''',
                       (data['make'], data['model'], data['year'], data['price'], car_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Car updated successfully!'})
    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM cars WHERE id = ?", (car_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Car deleted successfully!'})

if __name__ == '__main__':
    init_db()
    populate_db()
    app.run(debug=True)
    