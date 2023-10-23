from flask import Flask, render_template, jsonify, request
import openai
import time # REMOVE LATER
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
        # prompt = request.form['prompt']
        # res = {}
        # res['answer'] = "Hello! As a financial assistant, I can provide you with information and guidance on various financial topics. This includes but is not limited to:\n1. Budgeting: I can help you create and manage a budget to track your income and expenses effectively.\n2. Saving and investing: I can offer advice on savings strategies and investment options to help you grow your wealth.\n3. Debt management: I can provide tips on managing debt, including creating a repayment plan and strategies for reducing interest.\n4. Retirement planning: I can assist you in understanding retirement savings options such as 401(k), Individual Retirement Accounts (IRAs), and help you determine the best plan for your goals.\n5. Tax information: I can provide general information on tax-related topics, but for specific advice, it's recommended to consult a tax professional.\n6. Insurance: I can offer basic guidance on various types of insurance, such as health, life, auto, and home insurance."
        # time.sleep(0.05)
        # return jsonify(res), 200
        
        
        
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
