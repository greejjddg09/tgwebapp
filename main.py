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
    try:
        data = request.get_json()
        score = int(data['score'])
        player_id = str(data['player_id'])

        conn = sqlite3.connect('scores.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS scores (id INTEGER PRIMARY KEY AUTOINCREMENT, player_id TEXT, score INTEGER)')
        c.execute('INSERT INTO scores (player_id, score) VALUES (?, ?)', (player_id, score))
        conn.commit()
        conn.close()

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

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



