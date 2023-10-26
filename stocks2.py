import os
import requests
import sqlalchemy as db
import yfinance as yf
import pandas as pd
from sqlalchemy import text
import time
from ib_insync import *
# importing module
import time
import openai
import pandas as pd
import datetime


def create_db():
    # create database:
    engine = db.create_engine('sqlite:///atradebot.db', echo=True)
    connection = engine.connect()
    metadata = db.MetaData()

    # Update the "stocks" table with the desired attributes
    stocks = db.Table('stocks', metadata,
        db.Column('id', db.Integer(), primary_key=True),
        db.Column('symbol', db.String(255), nullable=False),  # Symbol is marked as non-nullable
        db.Column('sector', db.String(255), nullable=True),
        db.Column('date', db.Date(), nullable=False),  # Date is marked as non-nullable
        db.Column('close', db.Float(), nullable=True),
        db.Column('volume', db.Integer(), nullable=True),
        db.Column('open', db.Float(), nullable=True),  # Change "Open" to "open"
        db.Column('high', db.Float(), nullable=True),
        db.Column('low', db.Float(), nullable=True)
    )


    # create table in database:
    metadata.create_all(engine)
    return engine, connection, stocks

if __name__ == "__main__":
    import os

    # Delete the SQLite database file if it exists
    if os.path.exists('atradebot.db'):
        os.remove('atradebot.db')

    # Create a new database
    engine, connection, stocks = create_db()

    connection.execute(text("PRAGMA journal_mode=WAL"))

    # get list of stocks:
    stock_df = pd.read_excel('SP_500_Companies.xlsx')
    symbols = stock_df['Symbol'].tolist()

    # use YFinance to create a dataframe of all the stocks in the S&P 500
    # store each DF in Stocks table in the database
    today = datetime.date.today().strftime('%Y-%m-%d')

    for i in symbols[:5]:
        # get stock info
        try:
            ticker = yf.Ticker(i)
            stock_info = ticker.history(period='1d', start='2020-01-01', end=today)
            stock_info['symbol'] = i
            stock_info['date'] = today  # Change "Date" to lowercase "date"
            stock_info = stock_info[['symbol', 'date', 'Close', 'Volume', 'Open', 'High', 'Low']]  # Change "Date" to "date"
            stock_info.columns = ['symbol', 'date', 'Close', 'Volume', 'Open', 'High', 'Low']  # Change "Date" to "date"
            stock_info.to_sql('stocks', con=engine, if_exists='append', index=False)
            print(f"Added {i} to the database")
        except Exception as e:
            print(f"Could not add {i} to the database")
            print(e)
        time.sleep(1)
