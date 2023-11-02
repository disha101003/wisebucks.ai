import os
import requests
import sqlalchemy as db
import yfinance as yf
from sqlalchemy import text
import time
import pandas as pd
import datetime

def create_db():
    # Create database:
    engine = db.create_engine('sqlite:///atradebot.db', echo=True)
    connection = engine.connect()
    metadata = db.MetaData()

    # Update the "stocks" table with the desired attributes
    stocks = db.Table('stocks', metadata,
        db.Column('id', db.Integer(), primary_key=True), # Primary key
        db.Column('symbol', db.String(255), nullable=False),  # Symbol is marked as non-nullable
        db.Column('date', db.Date(), nullable=False),  
        db.Column('close', db.Float(), nullable=True),
        db.Column('volume', db.Integer(), nullable=True),
        db.Column('open', db.Float(), nullable=True),  
        db.Column('high', db.Float(), nullable=True),
        db.Column('low', db.Float(), nullable=True),
    )

    # Create table in the database:
    metadata.create_all(engine)
    return engine, connection, stocks

def update_db(engine, connection):
    # Get the list of stock symbols from the CSV
    stock_df = pd.read_csv('sp-500-index-10-29-2023.csv')
    symbols = stock_df['Symbol'].tolist()
    
    # Specify today's date
    today = datetime.date.today()
    
    for symbol in symbols:
        # Find the most recent date stored in the database for this symbol
        query = f"SELECT MAX(date) FROM stocks WHERE symbol = '{symbol}'"
        result = connection.execute(text(query)).fetchone()
        most_recent_date = result[0]
        
        if most_recent_date is None:
            # If no data exists for this symbol, start from a fixed date (e.g., '2020-01-01')
            start_date = datetime.date(2020, 1, 1)
        else:
            # If data exists, start from the day after the most recent date
            most_recent_date = datetime.datetime.strptime(most_recent_date, '%Y-%m-%d').date()
            start_date = most_recent_date + datetime.timedelta(days=1)
        
        if start_date <= today:
            try:
                stock_info = yf.download(symbol, start=start_date, end=today)  # API call to create DataFrame
                if not stock_info.empty:
                    stock_info['symbol'] = symbol
                    stock_info['date'] = stock_info.index.strftime('%Y-%m-%d')
                    stock_info = stock_info[['symbol', 'date', 'Close', 'Volume', 'Open', 'High', 'Low']]
                    stock_info.columns = ['symbol', 'date', 'close', 'volume', 'open', 'high', 'low']
                    
                    # Update the database with the new data
                    stock_info.to_sql('stocks', con=engine, if_exists='append', index=False, index_label='date')
                    
                    print(f"Updated {symbol} data from {start_date} to {today}")
                else:
                    print(f"No data available for {symbol} from {start_date} to {today}")
            except Exception as e:
                print(f"Could not update {symbol} data from {start_date} to {today}")
                print(e)
            time.sleep(1)
        else:
            print(f"Data for {symbol} is already up to date. Skipping.")

if __name__ == "__main__":
    # Check if the database exists and create it if not
    if not os.path.exists('atradebot.db'):
        create_db()
    else:
        engine, connection, _ = create_db()
    
    update_db(engine, connection)
