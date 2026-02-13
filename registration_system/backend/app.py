import os
import psycopg2
import time
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration from environment variables
class Config:
    DB_HOST = os.getenv("DB_HOST", "db")
    DB_NAME = os.getenv("DB_NAME", "registration_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            return psycopg2.connect(
                host=Config.DB_HOST,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASS
            )
        except Exception as e:
            logger.warning(f"Database connection failed, retrying... ({retries} left). Error: {e}")
            retries -= 1
            time.sleep(2)
    raise Exception("Could not connect to the database after multiple retries.")

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/status')
def status():
    return jsonify({
        "status": "success",
        "message": "Flask Backend is properly running!",
        "version": "1.1.0"
    }), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # 1. Validation
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password are required"}), 400
    
    if len(password) < 6:
        return jsonify({"status": "error", "message": "Password must be at least 6 characters long"}), 400

    try:
        # Ensure table is ready
        init_db()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 2. Check overlap
        cur.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cur.fetchone():
            return jsonify({"status": "error", "message": "User already exists"}), 409

        # 3. Proper Security: Hash the password
        hashed_password = generate_password_hash(password)

        # 4. Insert
        cur.execute(
            "INSERT INTO users (email, password) VALUES (%s, %s)",
            (email, hashed_password)
        )
        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"New user registered: {email}")
        return jsonify({"status": "success", "message": "User registered successfully"}), 201

    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, email, password FROM users ORDER BY id ASC")
        rows = cur.fetchall()
        
        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "email": row[1],
                "password": "[HASHED]" # Hide hashes in public list for better "proper" feel
            })
            
        cur.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
