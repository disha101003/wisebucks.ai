import os
import requests
import sqlalchemy as db
import yfinance as yf
import pandas as pd
from sqlalchemy import text
import time
from ib_insync import *

def create_db():
    # create database:
    engine = db.create_engine('sqlite:///atradebot.db', echo=True)
    connection = engine.connect()
    metadata = db.MetaData()

    # create a single table:
    stocks = db.Table('stocks', metadata,
                        db.Column('id', db.Integer(), primary_key=True),
                        db.Column('symbol', db.String(255), nullable=True),
                        db.Column('name', db.String(255), nullable=True),
                        db.Column('sector', db.String(255), nullable=True),
                        db.Column('industry', db.String(255), nullable=True),
                        db.Column('live_price', db.Float(), nullable=True),
                        db.Column('prev_close', db.Float(), nullable=True),
                        db.Column('open', db.Float(), nullable=True),
                        db.Column("volume", db.Integer(), nullable=True),
                    )
    news = db.Table('news', metadata,
                        db.Column('id', db.Integer(), primary_key=True),
                        db.Column('symbol', db.String(255), nullable=True),
                        db.Column('title', db.String(255), nullable=True),
                        db.Column('news_date', db.String(255), nullable=True),
                        db.Column('url', db.String(255), nullable=True),
                        db.Column('source', db.String(255), nullable=True),
                        db.Column('text', db.String(255), nullable=True),
                    )
    etfs = db.Table("etfs", metadata, 
                    db.Column("id", db.Integer(), primary_key=True),
                    db.Column("symbol", db.String(255), nullable=True),
                    db.Column('name', db.String(255), nullable=True),
                    db.Column('sector', db.String(255), nullable=True),
                    db.Column('industry', db.String(255), nullable=True),
                    db.Column('live_price', db.Float(), nullable=True),
                    db.Column('prev_close', db.Float(), nullable=True),
                    db.Column('open', db.Float(), nullable=True),
                    db.Column("volume", db.Integer(), nullable=True),
                    )
                    
    

    # create table in database:
    metadata.create_all(engine)
    return engine, connection, stocks, news

if __name__ == "__main__":
    engine, connection, stocks, news = create_db()

    connection.execute(text("PRAGMA journal_mode=DELETE"))

    # get list of stocks:
    stock_df = pd.read_excel('SP_500_Companies.xlsx')
    symbols = stock_df['Symbol'].tolist()

    ib = IB()
    ib.connect('127.0.0.1', 7496, clientId=1)
    news_providers = ib.reqNewsProviders()
    codes = '+'.join(news_provider.code for news_provider in news_providers)

    # get list of etfs (top 10)
    etfs_symbols = ["SPY", "IVV", "VOO", "VTI", "QQQ", "VEA", "VTV", "IEFA", "BND", "VUG"]

    # get data for symbols:
    for i in symbols[:5]:
        trans = connection.begin_nested()
        try:
            # get stock info
            try:
                ticker = yf.Ticker(i)
                info = ticker.info

                stock_values = {
                    "symbol": i,
                    'name': info.get('shortName', 'NA'),
                    'sector': info.get('sector', 'NA'),
                    'industry': info.get('industry', 'NA'),
                    'live_price': info.get('regularMarketPrice', 0.0),
                    'prev_close': info.get('previousClose', 0.0),
                    'open': info.get('open', 0.0),
                    'volume': info.get('volume', 0)
                }

                # Insert the stock into the database
                query_stock = db.insert(stocks)
                ResultProxy = connection.execute(query_stock, [stock_values])

            # Error handling for stock info fetching
            except requests.exceptions.HTTPError as error_terminal:
                print("HTTPError while fetching stock info for symbol:", i)
            except Exception as e:  # General exception catch
                print("Unexpected error while fetching stock info for symbol:", i)

            # Fetch and store news articles
            try:
                stock = Stock(i, 'SMART', 'USD')
                ib.qualifyContracts(stock)
                headlines = ib.reqHistoricalNews(stock.conId, codes, '', '', 100)

                for headline in headlines:
                    article_date = headline.time.date()
                    article = ib.reqNewsArticle(headline.providerCode, headline.articleId)

                    # Insert the article into the database
                    news_info = {
                        'symbol': i,
                        'title': '',  # Title not needed
                        'news_date': str(article_date),
                        'url': '',  # URL not provided
                        'source': '',  # Source not provided
                        'text': article.articleText
                    }

                    # Insert the news into the database
                    query_news = db.insert(news)
                    ResultProxy = connection.execute(query_news, [news_info])

            # Error handling for news fetching
            except requests.exceptions.HTTPError as error_terminal:
                print("HTTPError while fetching news for symbol:", i)
            except Exception as e:  # General exception catch
                print("Unexpected error while fetching news for symbol:", i)


            trans.commit()
            time.sleep(1)

        # Error handling
        except Exception as e:  # General exception catch
            print("Unexpected error:", e)
            trans.rollback()
    
    # get data for etf symbols
    for i in etfs_symbols:
        trans = connection.begin_nested()
        try: 
            try:
                #get etf info
                ticker = yf.Ticker(i)
                info = ticker.info()

                etf_values = {
                    "symbol": i,
                    'name': info.get('shortName', 'NA'),
                    'sector': info.get('sector', 'NA'),
                    'industry': info.get('industry', 'NA'),
                    'live_price': info.get('regularMarketPrice', 0.0),
                    'prev_close': info.get('previousClose', 0.0),
                    'open': info.get('open', 0.0),
                    'volume': info.get('volume', 0)
                }

                # Insert etfs into the database:
                query_etf = db.insert(etfs)
                ResultProxy = connection.execute(query_etf, [etf_values])

            # Error handling for ETF info fetching:
            except requests.exceptions.HTTPError as error_terminal:
                print("HTTPError while fetching stock info for symbol:", i)
            except Exception as e:  # General exception catch
                print("Unexpected error while fetching stock info for symbol:", i)

            trans.commit()
            time.sleep(1)
        # Error handling:
        except Exception as e:  # General exception catch
            print("Unexpected error:", e)
            trans.rollback()


    # Fetch and print the first 5 stocks from the database after processing
    #query = db.select([data]).limit(5)
    query = stocks.select().limit(5)
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()

    for result in ResultSet:
        print(result)

    connection.execute(text("PRAGMA journal_mode=WAL"))

    # Close the connection
    connection.close()
