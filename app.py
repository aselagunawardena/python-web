from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display():
    text = request.form.get('text', '')
    return render_template('index.html', displayed_text=text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
