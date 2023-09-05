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


# This is an LLMChain to create a task for a particular exam

llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")
template = """You are a test task creator for {test_type}. I will provide you the test type and your job is to create a task for a test taker.

You will provide a topic and ask the user if they agree or disagree, provide pros and cons etc and provide their views on the topic.

Sample Tasks for {test_type}
Sample 1: Technology
Task: "Some people believe that technological advancements lead to the loss of traditional cultures. To what extent do you agree or disagree?"

Sample 2: Education
Task: "Some educators argue that every child should be taught how to play a musical instrument. Discuss the advantages and disadvantages of this. Give your own opinion."

Sample 3: Environment
Task: "Climate change is now an accepted threat to our planet, but there is not enough political action to control excessive consumerism and pollution. Discuss both views and give your own opinion."

Sample 4: Health
Task: "Some people think that governments should focus on reducing healthcare costs, rather than funding arts and sports. Do you agree or disagree?"

Sample 5: Society
Task: "Some people think that the best way to reduce crime is to give longer prison sentences. Others, however, believe there are better alternative ways of reducing crime. Discuss both views and give your opinion."

Sample 6: Work
Task: "Remote work is becoming increasingly popular. Discuss the advantages and disadvantages of working from home."

Sample 7: Global Issues
Task: "Some people argue that developed countries have a higher obligation to combat climate change than developing countries. Discuss both sides and give your own opinion."

Sample 8: Science
Task: "Genetic engineering is an important issue in modern society. Some people think that it will improve people’s lives in many ways. Others feel that it may be a threat to life on earth. Discuss both these views and give your own opinion."

You will use the above examples only as a guideline for framing the task and create a new task and description randomly on a different topic. No need to use the word Sample in the task description. 

Create 5 such tasks and descriptions based on the above guidelines. In your output mention these ten tasks and format the output as Title:  and Description: .
"""
prompt_template = PromptTemplate(input_variables=["test_type"], template=template)
task_creator_chain = LLMChain(llm=llm, prompt=prompt_template)

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

template = """You are a test task selector. I will provide you a list of five tasks and their respective descriptions below. 

{five_tasks}

You will select one of the tasks randomly and output it along with its description in a json format that has the following fields:

"title": "picked randomly from the ten tasks",
"description": "description for the randomly picked title"
"""

prompt_template = PromptTemplate(input_variables=["five_tasks"], template=template)
task_selector_chain = LLMChain(llm=llm, prompt=prompt_template)

# print(task_selector_chain.run(writing_task))

# This is the overall chain where we run these two chains in sequence.
from langchain.chains import SimpleSequentialChain
overall_chain = SimpleSequentialChain(chains=[task_creator_chain, task_selector_chain], verbose=True)

# print(overall_chain.run("IELTS Academic Writing Task 2"))

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def hello_world():
    return jsonify({"message": "Hello World"})

# API endpoint for generating a test
@app.route('/api/generate_test', methods=['POST'])
def api_generate_test():
    generated_data = overall_chain.run("IELTS Academic Writing Task 2")
    try:
        generated_data = json.loads(generated_data)
    except (json.JSONDecodeError, TypeError):
        pass

    if isinstance(generated_data, dict):
        title = generated_data.get('title', 'Default Title')
        description = generated_data.get('description', 'Default Description')
        test_data = {
            'title': title,
            'description': description
        }
        return jsonify(test_data)
    else:
        return jsonify({'error': 'Unexpected data format'})
    
if __name__ == '__main__':
    app.run(debug=True)