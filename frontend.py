# frontend.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Home route to render the input form
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission and call FastAPI backend
@app.route('/generate', methods=['POST'])
def generate():
    description = request.form['description']
    response = requests.post('http://localhost:8000/generate/', json={'description': description})
    if response.status_code == 200:
        plantuml = response.json().get('plantuml', '')
        return jsonify({'plantuml': plantuml})
    else:
        return jsonify({'error': 'Failed to generate PlantUML code'}), 500

if __name__ == '__main__':
    app.run(debug=True)
