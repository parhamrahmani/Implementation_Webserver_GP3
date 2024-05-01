from flask import Flask, request, jsonify, send_from_directory, render_template_string
import pymysql.cursors
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
messages = []


@app.route('/board', methods=['GET'])
def get_messages():
    return jsonify(messages)


@app.route('/board', methods=['POST'])
def post_message():
    message = request.json.get('message', '')
    messages.append(message)  # Append new message to list
    return jsonify(messages)


@app.route('/board_page')
def board_page():
    return send_from_directory(app.static_folder, 'board.html')


# Serve static file for login and registration on localhost:5000/
@app.route('/')
def home():
    print("Serving index.html from:", os.path.join(app.static_folder, 'index.html'))
    return send_from_directory(app.static_folder, 'login.html')


# Get database connection
def get_db_connection():
    password = os.getenv('MYDB_PASS', '#Pass@pass')  # In case that environment variable is not set
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
            # # Hypothetical more vulnerable code
            cursor.execute(f"SELECT * FROM credentials WHERE user = '{username}'")
            # cursor.execute("SELECT password FROM credentials WHERE user = %s", (username,))
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
            # # Hypothetical more vulnerable code
            cursor.execute(f"SELECT * FROM credentials WHERE user = '{username}'")
            # cursor.execute("SELECT * FROM credentials WHERE user = %s", (username,))
            if cursor.fetchone():
                return jsonify({'message': 'User already exists'}), 409
                # !! Vulnerable Code : SQL Injection !!
            # # Hypothetical more vulnerable code
            cursor.execute(f"INSERT INTO credentials (user, password) VALUES ('{username}', '{password}')")

            # cursor.execute("INSERT INTO credentials (user, password) VALUES (%s, %s)",
            #    (username, password))
            connection.commit()
            return jsonify({'message': 'User created successfully'}), 201
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
