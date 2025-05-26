from flask import Flask, request, jsonify
import sqlite3
import datetime
import os

app = Flask(__name__)

# Создание базы данных и таблицы при первом запуске
def init_db():
    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Backend работает!"

@app.route("/submit_score", methods=["POST"])
def submit_score():
    data = request.get_json()
    username = data.get("username")
    score = data.get("score")

    if not username or score is None:
        return jsonify({"status": "error", "message": "Missing username or score"}), 400

    timestamp = datetime.datetime.utcnow().isoformat()

    conn = sqlite3.connect('scores.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (username, score, timestamp) VALUES (?, ?, ?)",
                   (username, score, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "message": "Score saved"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


