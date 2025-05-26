from flask import Flask, request
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешаем CORS

# Создание таблицы при старте
def init_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            score INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    user_id = data.get('user_id')
    username = data.get('username')
    score = data.get('score')
    timestamp = datetime.now().isoformat()

    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (user_id, username, score, timestamp) VALUES (?, ?, ?, ?)',
              (user_id, username, score, timestamp))
    conn.commit()
    conn.close()
    return {'status': 'success'}

@app.route('/')
def home():
    return "Backend is running!"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=10000)

