from flask import Flask, send_file, send_from_directory, jsonify
import json_converter
import time

app = Flask(__name__)
BOOT_ID = str(time.time())

@app.route('/')
@app.route('/main')
def index():
    return send_file('Jeopardy_main.html')

@app.route('/gameboard')
def gameboard():
    return send_file('Jeopardy_gameboard.html')

@app.route('/final')
def final():
    return send_file('Jeopardy_final.html')

@app.route('/teams')
def teams():
    return send_file('teams.html')

@app.route('/style.css')
def style():
    return send_file('style.css', mimetype='text/css')

@app.route('/images/<path:filename>')
def images(filename):
    return send_from_directory('images', filename)

@app.route('/audio/<path:filename>')
def audio(filename):
    return send_from_directory('audio', filename)

@app.route('/answers.json')
def answers_json():
    return send_file('answers.json', mimetype='application/json')

@app.route('/players.json')
def players_json():
    return send_file('players.json', mimetype='application/json')

@app.route('/api/boot-id')
def boot_id():
    return jsonify({'boot_id': BOOT_ID})

if __name__ == '__main__':
    json_converter.convert_to_json()
    app.run(debug=True)
