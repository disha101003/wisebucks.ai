# Wisebucks.AI

This is a FinTech project, in which we are trying to make a comprehensive app / website for FinTech queries as well as portfolio generation.

1. This project recognize that to predict accurate and most profitable portfolios, we need to take into account :
    1. Historical stock prices
    2. Current news related to the stocks
    3. Financial ratios like price-to-earnings, PEG, price-to-sales, price-to-book, and debt-to-equity
        
        Traditionally, LSTMs have been used for stock predictions but they only take into account the historical stock prices, but for accurate predictions it is more important to factor in the current news surrounding these stocks.
        
        Therefore, this project proposes :
        
        1. The use of LLMs on news to do sentiment analysis for each news article for a particular stock in S&P 500.
        2. Monte Carlo / LSTMs / Regression Models for the historical data of stock prices
        3. Assign different weights to these financial ratios which tells how positively or negatively this reflects on the particular stock
        
        Then weigh all these three different aspects for a particular stock into a final score for each stock that will then be used for stock portfolio generation.
        
2. This project also proposes the development of a paper trading platform in python as an added feature for the website.
3. This project also proposes a chatbot feature, to answer general queries related to FinTech using a Large language model.
4. This project proposed the use of yfinance api, trader workstation to get the required data, store it in SQL database and then retrieve data from this database for the purpose of training the data.
5. In the beginning, the project proposes to use open source LLMs such as OpenAI’s API for its alpha model, but later on we plan to develop our own LLM model for the chatbot and sentiment analysis on news.

Deployed Link: https://flask-production-0003.up.railway.app/


The below is the demo for our project:


https://github.com/user-attachments/assets/821877ae-5ef2-47b1-8b7c-63189970c35d



Thank you Professor Eugenio Culurciello and Sankalp Krishnan for your guidance throughout this project!
