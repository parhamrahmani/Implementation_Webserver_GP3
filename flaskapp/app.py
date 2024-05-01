from flask import Flask, request, jsonify, send_from_directory
import pymysql.cursors
import os
from flask_cors import CORS

# Create an instance of the Flask class
app = Flask(__name__)

# Enable CORS --> Cross-Origin Resource Sharing
CORS(app)


# Serve static file for login and registration on localhost:5000/
@app.route('/')
def home():
    print("Serving index.html from:", os.path.join(app.static_folder, 'index.html'))
    return send_from_directory(app.static_folder, 'login.html')


# Get database connection
def get_db_connection():
    password = os.getenv('MYDB_PASS', 'your_password')  # In case that environment variable is not set
    return pymysql.connect(host='localhost',
                           user='admin',
                           password=password,
                           database='mydb',
                           cursorclass=pymysql.cursors.DictCursor)


# Test database connection
@app.route('/test_db')
def test_db():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        return f"Database connection successful: {result}"
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500
    finally:
        if connection:
            connection.close()


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # !! Vulnerable Code : SQL Injection !!
            cursor.execute("SELECT password FROM credentials WHERE user = %s", (username,))
            result = cursor.fetchone()
            if result and result['password'] == password:
                return jsonify({'message': 'Login successful'}), 200
            else:
                return jsonify({'message': 'Invalid credentials'}), 401
    finally:
        connection.close()


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            # !! Vulnerable Code : SQL Injection !!

            cursor.execute("SELECT * FROM credentials WHERE user = %s", (username,))
            if cursor.fetchone():
                return jsonify({'message': 'User already exists'}), 409
                # !! Vulnerable Code : SQL Injection !!

            cursor.execute("INSERT INTO credentials (user, password) VALUES (%s, %s)",
                           (username, password))
            connection.commit()
            return jsonify({'message': 'User created successfully'}), 201
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
