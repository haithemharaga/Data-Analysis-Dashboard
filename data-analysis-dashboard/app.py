from flask import Flask, render_template, request
import sqlite3
import os

# Initialize the Flask app
app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    try:
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Create the sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                date TEXT,
                product TEXT,
                quantity INTEGER,
                price REAL
            )
        ''')
        
        # Insert sample data (optional)
        cursor.execute('''
            INSERT INTO sales (date, product, quantity, price)
            VALUES 
                ('2023-10-01', 'Product A', 10, 19.99),
                ('2023-10-02', 'Product B', 5, 29.99),
                ('2023-10-03', 'Product C', 8, 9.99)
        ''')
        
        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()

# Initialize the database
initialize_database()

# Function to connect to the database and fetch data
def get_data():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales')
    data = cursor.fetchall()
    conn.close()
    return data

# Function to fetch filtered data
def get_filtered_data(start_date, end_date):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sales WHERE date BETWEEN ? AND ?', (start_date, end_date))
    data = cursor.fetchall()
    conn.close()
    return data

# Route for the homepage
@app.route('/')
def index():
    data = get_data()
    dates = [row[1] for row in data]
    quantities = [row[3] for row in data]
    return render_template('index.html', data=data, dates=dates, quantities=quantities)

# Route for filtering data
@app.route('/filter', methods=['POST'])
def filter_data():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    filtered_data = get_filtered_data(start_date, end_date)
    dates = [row[1] for row in filtered_data]
    quantities = [row[3] for row in filtered_data]
    return render_template('index.html', data=filtered_data, dates=dates, quantities=quantities)
def initialize_database():
    try:
        # Connect to the SQLite database (creates it if it doesn't exist)
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        
        # Create the sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY,
                date TEXT,
                product TEXT,
                quantity INTEGER,
                price REAL
            )
        ''')
        
        # Insert sample data
        cursor.execute('''
            INSERT INTO sales (date, product, quantity, price)
            VALUES 
                ('2023-10-01', 'Product A', 10, 19.99),
                ('2023-10-02', 'Product B', 5, 29.99),
                ('2023-10-03', 'Product C', 8, 9.99)
        ''')
        
        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()
            
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)