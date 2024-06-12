from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import pymysql.cursors
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = 'your_secret_key'  # Replace with your secret key

messages = []

@app.route('/board/<username>', methods=['GET'])
def get_messages(username):
    return jsonify(messages)

@app.route('/board/<username>', methods=['POST'])
def post_message(username):
    message = request.json.get('message', '')
    messages.append({'username': username, 'message': message})
    return jsonify(messages)

@app.route('/board_page/<username>')
def board_page(username):
    return send_from_directory(app.static_folder, 'board.html')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'login.html')

def get_db_connection():
    password = os.getenv('MYDB_PASS', 'password')
    return pymysql.connect(host='localhost',
                           user='admin',
                           password=password,
                           database='mydb',
                           cursorclass=pymysql.cursors.DictCursor)

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
            cursor.execute(f"SELECT * FROM credentials WHERE user = '{username}'")
            result = cursor.fetchone()
            if result and result['password'] == password:
                print(f"User {username} logged in successfully")
                return jsonify({'message': 'Login successful', 'username': username}), 200
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
            cursor.execute(f"SELECT * FROM credentials WHERE user = '{username}'")
            if cursor.fetchone():
                return jsonify({'message': 'User already exists'}), 409

            cursor.execute(f"INSERT INTO credentials (user, password) VALUES ('{username}', '{password}')")
            connection.commit()
            return jsonify({'message': 'User created successfully'}), 201
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
