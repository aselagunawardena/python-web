from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'car-game-demo-key'

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/about')
def about():
    return send_from_directory('templates', 'about.html')

@app.route('/graph-fun')
def graph_fun():
    return send_from_directory('templates', 'graph_fun.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
