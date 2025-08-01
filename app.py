from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime
from werkzeug.security import check_password_hash

app = Flask(__name__)

def get_db_connection():
return psycopg2.connect(
host=os.getenv("DB_HOST"),
port=os.getenv("DB_PORT"),
dbname=os.getenv("DB_NAME"),
user=os.getenv("DB_USER"),
password=os.getenv("DB_PASSWORD")
)

@app.route("/login", methods=["POST"])
def login():
data = request.get_json()
username = data.get("username")
password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM utilizadores WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            return jsonify({"user_id": user[0]}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/location", methods=["POST"])
def receive_location():
data = request.get_json()
user_id = data.get("user_id")
latitude = data.get("latitude")
longitude = data.get("longitude")
precisao = data.get("precisao")
timestamp = data.get("timestamp") or datetime.utcnow().isoformat()

    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400
    if latitude is None or longitude is None:
        return jsonify({"error": "latitude and longitude are required"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO localizacoes (user_id, latitude, longitude, precisao, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, latitude, longitude, precisao, timestamp)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
return "OREX API running."

if __name__ == "__main__":
app.run(host="0.0.0.0", port=8000)