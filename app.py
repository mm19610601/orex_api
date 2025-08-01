from flask import Flask, request, jsonify
import psycopg2
import os
from datetime import datetime
from urllib.parse import urlparse

app = Flask(__name__)

def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    result = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

@app.route("/location", methods=["POST"])
def receive_location():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    timestamp = data.get("timestamp") or datetime.utcnow().isoformat()
    user_id = data.get("user_id")  # opcional

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO locations (user_id, latitude, longitude, timestamp) VALUES (%s, %s, %s, %s)",
            (user_id, latitude, longitude, timestamp)
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def index():
    return "OREX API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
