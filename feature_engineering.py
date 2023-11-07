import sqlalchemy as db
import pandas as pd

# Function to create a database connection
def connect_to_db():
    engine = db.create_engine('sqlite:///atradebot.db', echo=True)
    connection = engine.connect()
    return connection

def generate_features(df):
    # Calculate daily returns
    df['daily_return'] = df['close'].pct_change(periods=1)

    # 5-day rolling averages for close price and volume
    df['5_day_mean_close_price'] = df['close'].rolling(5).mean()
    df['5_day_mean_volume'] = df['volume'].rolling(5).mean()

    # Calculate daily range and volatility
    df['daily_range'] = df['high'] - df['low']
    df['volatility'] = df['daily_return'].rolling(5).std()

    # Create a new column called Quarter
    df['quarter'] = pd.PeriodIndex(df['date'], freq='Q').astype(str)

    # Fill missing values
    df['5_day_mean_close_price'] = df['5_day_mean_close_price'].fillna(0)
    df['5_day_mean_volume'] = df['5_day_mean_volume'].fillna(0)
    df['volatility'] = df['volatility'].fillna(0)
    df['daily_return'] = df['daily_return'].fillna(0)

    # Calculate 5-day and 20-day exponential moving averages for closing price
    df['EMA_Close_5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA_Close_20'] = df['close'].ewm(span=20, adjust=False).mean()

    return df

def feature_engineering(connection, symbol):
    # Fetch the data for the symbol
    query = f"SELECT * FROM stocks WHERE symbol = '{symbol}'"
    data = pd.read_sql(query, connection)

    # Apply feature engineering to the data
    engineered_data = generate_features(data)

    # Add these newly added columns from generate_features() to the stocks table 
    engineered_data.to_sql('stocks', con=connection, if_exists='replace', index=False, index_label='date')