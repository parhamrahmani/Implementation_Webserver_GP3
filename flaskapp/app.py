from flask import Flask, request, jsonify, send_from_directory
import pymysql.cursors
import os
import bcrypt
from flask_cors import CORS

# Create an instance of the Flask class
app = Flask(__name__)

# Enable CORS --> Cross-Origin Resource Sharing
CORS(app)


# serve static file for login on localhost:5000/
@app.route('/')
def home():
    print("Serving index.html from:", os.path.join(app.static_folder, 'index.html'))
    return send_from_directory(app.static_folder, 'login.html')


# serve static file for register on localhost:5000/register
@app.route('/register')
def register_page():
    return send_from_directory('static', 'register.html')


#get database connection
def get_db_connection():
    password = os.getenv('MYDB_PASS')
    return pymysql.connect(host='localhost',
                           user='admin',
                           password=password,
                           database='mydb',
                           cursorclass=pymysql.cursors.DictCursor)


# test database connection
# use curl localhost:5000/test_db for testing
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

    password = password.encode('utf-8')
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM credentials WHERE user = %s", (username,))
            result = cursor.fetchone()
            if result and bcrypt.checkpw(password, result['password'].encode('utf-8')):
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

    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM credentials WHERE user = %s", (username,))
            if cursor.fetchone():
                return jsonify({'message': 'User already exists'}), 409

            cursor.execute("INSERT INTO credentials (user, password) VALUES (%s, %s)",
                           (username, hashed_password.decode('utf-8')))
            connection.commit()
            return jsonify({'message': 'User created successfully'}), 201
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
