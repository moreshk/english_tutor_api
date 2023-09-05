from flask import Flask, jsonify, request
import json
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()

# Fetch the OPENAI_API_KEY from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY in the .env file.")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def hello_world():
    return jsonify({"message": "Hello World"})

if __name__ == '__main__':
    app.run(debug=True)
