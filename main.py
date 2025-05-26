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
    user_id = data.get('user_id')
    score = data.get('score')

    if user_id is None or score is None:
        return {'status': 'error', 'message': 'Неверные данные'}, 400

    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (user_id, score) VALUES (?, ?)', (user_id, score))
    conn.commit()
    conn.close()

    return {'status': 'success'}
@app.route('/get_scores', methods=['GET'])
def get_scores():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY id DESC LIMIT 10')
    results = c.fetchall()
    conn.close()
    return {'scores': results}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)



