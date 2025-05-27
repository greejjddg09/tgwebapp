from flask import Flask, request, jsonify
import sqlite3
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Инициализация базы данных

def init_db():
    # Удаляем старую базу, если она есть
    if os.path.exists('scores.db'):
        os.remove('scores.db')

    # Создаем заново с нужными полями
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id TEXT,
            username TEXT,
            score INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Создаем базу при запуске
init_db()


@app.route('/')
def home():
    return 'Backend работает!'


@app.route('/get_scores', methods=['GET'])
def get_scores():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY id DESC LIMIT 10')
    results = c.fetchall()
    conn.close()

    return {
        'scores': [
            {
                'id': row[0],
                
                'score': row[3]
            }
            for row in results
        ]
    }


@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.get_json()
    if not data or  'score' not in data:
        return jsonify({"error": "Missing player_id, username or score"}), 400

    player_id = data['player_id']
    username = data['username']
    score = data['score']

    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores ( score) VALUES (?, ?, ?)', (player_id, username, score))
    conn.commit()
    conn.close()

    return jsonify({"message": "Score saved successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
