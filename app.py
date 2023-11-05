from flask import Flask, render_template, jsonify, request
import openai
from getpass import getpass
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")


def page_not_found(e):
    return render_template('404.html'), 404


app = Flask(__name__)

app.register_error_handler(404, page_not_found)


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        question = request.form['prompt']
        template = """Financial Query: {question}
    Response: """
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm = OpenAI()
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        answer = llm_chain.run(question)
        return jsonify(answer=answer)
          
    return render_template('home.html', **locals())


@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
