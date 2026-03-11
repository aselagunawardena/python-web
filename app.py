from flask import Flask, jsonify, request, send_from_directory
import os

from flask import session, make_response
import math

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = 'car-game-demo-key'  # Needed for session

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('templates', 'index.html')


@app.route('/about')
def about():
    """Serve a simple About page that teaches routes"""
    return send_from_directory('templates', 'about.html')


@app.route('/graph-fun')
def graph_fun():
    """Serve the Graph Fun interactive visualization page"""
    return send_from_directory('templates', 'graph_fun.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
