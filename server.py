from flask import Flask, send_file, send_from_directory

app = Flask(__name__)

@app.route('/')
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

if __name__ == '__main__':
    app.run(debug=True)
