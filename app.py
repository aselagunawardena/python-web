from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('templates', 'index.html')


@app.route('/about')
def about():
    """Serve a simple About page that teaches routes"""
    return send_from_directory('templates', 'about.html')

@app.route('/api/display', methods=['POST'])
def display_text():
    """API endpoint - receives text and returns it as JSON"""
    data = request.get_json()
    text = data.get('text', '')
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
