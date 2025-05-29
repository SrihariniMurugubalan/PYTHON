from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'feedbacks.json'

@app.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = load_feedbacks()
    return jsonify(feedbacks)

@app.route('/feedbacks', methods=['POST'])
def add_feedback():
    data = request.json
    print(request.json)
    if not data or 'user' not in data or 'comment' not in data or 'rating' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    feedbacks = load_feedbacks()

    new_feedback = {
        "id": len(feedbacks) + 1,
        "user": data['user'],
        "comment": data['comment'],
        "rating": data['rating']
    }
    feedbacks.append(new_feedback)
    save_feedbacks(feedbacks)
    return jsonify(new_feedback), 201

def load_feedbacks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)
    
def save_feedbacks(feedbacks):
    with open(DATA_FILE, 'w') as f:
        json.dump(feedbacks, f, indent=2)

if __name__ == '__main__':
    app.run(debug=True)
