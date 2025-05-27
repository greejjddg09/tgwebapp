from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return 'Backend работает!'


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    if not data or 'player_id' not in data or 'score' not in data:
        return jsonify({"error": "Missing player_id or score"}), 400

    player_id = data['player_id']
    score = data['score']

    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (player_id, score) VALUES (?, ?)', (player_id, score))
    conn.commit()
    conn.close()

    return jsonify({"message": "Score saved successfully"}), 200





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)



