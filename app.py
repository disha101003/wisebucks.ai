from flask import Flask, render_template, jsonify, request
import yfinance as yf
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


@app.route('/')
def index():
    return render_template('home.html', **locals())


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        question = request.form['prompt']
        template = """Stock-related Query: {question}
    Response: """
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm = OpenAI()
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        answer = llm_chain.run(question)
        return jsonify(answer=answer)
    return render_template('chatbot.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/investment')
def investment():
    return render_template('investment.html')

@app.route('/trading')
def trading():
    return render_template('trading.html')

@app.route('/wisewealth')
def wisewealth():
    return render_template('wisewealth.html')

@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    ticker = request.get_json()['ticker']
    data = yf.Ticker(ticker).history(period='1y')
    return jsonify({'currentPrice':data.iloc[-1].Close,
                    'openPrice':data.iloc[-1].Open})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
