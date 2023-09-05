from flask import Flask, jsonify, request
import json
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def hello_world():
    return jsonify({"message": "Hello World"})

if __name__ == '__main__':
    app.run(debug=True)
