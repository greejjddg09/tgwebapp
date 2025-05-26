from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "scores.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                score INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route("/submit-score", methods=["POST"])
def submit_score():
    data = request.json
    username = data.get("username")
    score = data.get("score")

    if not username or score is None:
        return jsonify({"error": "Missing username or score"}), 400

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
        conn.commit()

    return jsonify({"message": "Score saved"}), 200

init_db()

if __name__ == "__main__":
    app.run(debug=True)

