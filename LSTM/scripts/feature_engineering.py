import sqlalchemy as db
import pandas as pd
import pandas_ta as ta

# Function to create a database connection
def connect_to_db():
    engine = db.create_engine('sqlite:///atradebot.db', echo=True)
    connection = engine.connect()
    return connection

def generate_features(df):
    # Calculate daily returns
    df['daily_return'] = df['close'].pct_change(periods=1)

    # Calculate daily range and volatility
    df['daily_range'] = df['high'] - df['low']

    # Create a new column called Quarter
    df['quarter'] = pd.PeriodIndex(df['date'], freq='Q').astype(str)

    # Calculate 5-day and 20-day exponential moving averages for closing price
    df['EMA_Close_5'] = df['close'].ewm(span=5).mean()
    df['EMA_Close_20'] = df['close'].ewm(span=20).mean()

    #df['volatility'] = df['volatility'].fillna(0)
    df['daily_return'] = df['daily_return'].fillna(0)

    # Adding indicators
    df['RSI']=ta.rsi(df.close, length=15)
    df['EMAF']=ta.ema(df.close, length=20)
    df['EMAM']=ta.ema(df.close, length=100)
    df['EMAS']=ta.ema(df.close, length=150)

    # for column RSI, fill the NaN values with that column's mean
    df['RSI'] = df['RSI'].fillna(df['RSI'].mean())

    # for column EMAF, fill the NaN values with that column's mean
    df['EMAF'] = df['EMAF'].fillna(df['EMAF'].mean())

    # for column EMAM, fill the NaN values with that column's mean
    df['EMAM'] = df['EMAM'].fillna(df['EMAM'].mean())

    # for column EMAS, fill the NaN values with that column's mean
    df['EMAS'] = df['EMAS'].fillna(df['EMAS'].mean())



    df['TargetNextClose'] = df['adj_close'].shift(-1) # adjusted close price for the next day

    return df

def feature_engineering(connection, symbol):
    # Fetch the data for the symbol
    query = f"SELECT * FROM stocks WHERE symbol = '{symbol}'"
    data = pd.read_sql(query, connection)

    # Apply feature engineering to the data
    engineered_data = generate_features(data)

    # Add these newly added columns from generate_features() to the stocks table 
    engineered_data.to_sql('stocks', con=connection, if_exists='replace', index=False, index_label='date')