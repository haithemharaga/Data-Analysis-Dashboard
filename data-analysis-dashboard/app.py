from flask import Flask, render_template
import sqlite3

# Initialize the Flask app
app = Flask(__name__)

# Function to connect to the database and fetch data
def get_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Query the database
    cursor.execute('SELECT * FROM sales')
    data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Return the fetched data
    return data

# Route for the homepage
@app.route('/')
def index():
    # Fetch data from the database
    data = get_data()

    # Prepare data for the chart
    dates = [row[1] for row in data]  # Extract dates (assuming date is in the 2nd column)
    quantities = [row[3] for row in data]  # Extract quantities (assuming quantity is in the 4th column)

    # Pass the data to the HTML template
    return render_template('index.html', data=data, dates=dates, quantities=quantities)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)