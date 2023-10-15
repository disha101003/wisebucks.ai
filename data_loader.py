import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import datetime

"""
TEST COMMIT
"""

def fetch_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    # change Date Column to datetime
    print(data.info())
    return data.reset_index().drop(['Adj Close'], axis=1)


def update_data(df, recent_data_df):
    # Get the most recent date in the existing dataset
    last_date_in_df = pd.to_datetime(df['Date']).max()

    # Filter the recent_data_df to include only data from the last date in the existing dataset
    recent_data_df = recent_data_df[recent_data_df['Date'] > last_date_in_df]

    # Concatenate the existing dataset with the recent data
    updated_df = pd.concat([df, recent_data_df], ignore_index=True)

    # make Date column datetime
    updated_df['Date'] = pd.to_datetime(updated_df['Date'])

    # Sort the updated dataset by date
    updated_df = updated_df.sort_values(by='Date', ascending=True).reset_index(drop=True)

    return updated_df


def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def generate_features(df):

    # Calculate daily returns
    df['Daily_Return'] = df['Close'].pct_change(periods=1)

    # 5-day rolling averages for close price and volume
    df['5_day_mean_close_price'] = df['Close'].rolling(5).mean()
    df['5_day_mean_volume'] = df['Volume'].rolling(5).mean()

    # Calculate daily range and volatility
    df['Daily_Range'] = df['High'] - df['Low']
    df['Volatility'] = df['Daily_Return'].rolling(5).std()

    # Create a new column called Quarter
    df['Quarter'] = pd.PeriodIndex(df['Date'], freq='Q')

    # Fill missing values
    df['5_day_mean_close_price'] = df['5_day_mean_close_price'].fillna(0)
    df['5_day_mean_volume'] = df['5_day_mean_volume'].fillna(0)
    df['Volatility'] = df['Volatility'].fillna(0)
    df['Daily_Return'] = df['Daily_Return'].fillna(0)

    # Calculate 5-day and 20-day exponential moving averages for closing price
    df['EMA_Close_5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['EMA_Close_20'] = df['Close'].ewm(span=20, adjust=False).mean()

    return df

def scale_data(df, features_to_scale, scaler_directory='/Users/anujthakkar/Documents/Purdue/Projects/Stock Market/flask_app/data/scalers'):
    import joblib
    import os

    """Scale numerical features using MinMaxScaler."""
    scaler = MinMaxScaler()
    df[features_to_scale] = scaler.fit_transform(df[features_to_scale])

    scaler_filename = 'features_scaler.save'
    scaler_path = os.path.join(scaler_directory, scaler_filename)
    joblib.dump(scaler, scaler_path)
    return df

def save_data(df, output_file):
    """Save the processed DataFrame to a new CSV file."""
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    # Define file paths
    input_file = '/Users/anujthakkar/Documents/Purdue/Projects/Stock Market/flask_app/data/AAPL.csv'
    output_file = '/Users/anujthakkar/Documents/Purdue/Projects/Stock Market/flask_app/data/clean/AAPL_feature_engineered.csv'

    # Define numerical features to scale
    numerical_features = ['Volume', 'Open', 'High', 'Low', 'Daily_Return',
                          '5_day_mean_close_price', '5_day_mean_volume', 'Daily_Range',
                          'Volatility', 'EMA_Close_5', 'EMA_Close_20']

    # Load data
    apple_df = load_data(input_file)

    # Fetch recent data
    # Calculate start_date and end_date based on existing data and current date
    start_date = (pd.to_datetime(apple_df['Date']).max() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    recent_data_df = fetch_stock_data('AAPL', start_date, end_date)

    # Update the existing dataset with the recent data
    apple_df = update_data(apple_df, recent_data_df)

    # write to csv
    apple_df.to_csv(input_file, index=False)

    """ we want to predict the closing price of the stock for the next 5 days.
        Simulate future data for the next 5 business days and append it to the existing dataset.
    """ 

    # Calculate the next 5 business days
    next_5_days = pd.bdate_range(end_date, periods=5, freq='C')

    # Create a new DataFrame with the next 5 business days
    future_dates_df = pd.DataFrame({'Date': next_5_days})

    # Initialize other feature columns for the future dates (you may adjust these based on your assumptions)
    future_dates_df['Open'] = apple_df['Close'].iloc[-1]  # Assume 'Open' equals the last 'Close' value
    future_dates_df['High'] = apple_df['Close'].iloc[-1]  # Assume 'High' equals the last 'Close' value
    future_dates_df['Low'] = apple_df['Close'].iloc[-1]   # Assume 'Low' equals the last 'Close' value
    future_dates_df['Volume'] = 0  # You may set an appropriate value based on your assumptions

    # Generate synthetic 'Close' prices based on the last available 'Close' price and a daily return assumption
    # Here, we assume a constant daily return for simplicity; you can modify this assumption
    # to match your desired trend or pattern
    last_close_price = apple_df['Close'].iloc[-1]
    daily_return_assumption = 0.01  # Adjust this value based on your assumption (e.g., 1% daily return)
    synthetic_close_prices = [last_close_price * (1 + daily_return_assumption ** i) for i in range(1, 6)]

    # Assign the generated 'Close' prices to the future dates DataFrame
    future_dates_df['Close'] = synthetic_close_prices


    # Assign the generated 'Close' prices to the future dates DataFrame
    future_dates_df['Close'] = synthetic_close_prices

    # Append the future dates DataFrame to the existing dataset
    apple_df = pd.concat([apple_df, future_dates_df], ignore_index=True)

    # Feature engineering (you can also generate additional features for the future dates)
    apple_df = generate_features(apple_df)

    # Fill missing values in the DataFrame (e.g., for newly generated features)
    apple_df = apple_df.fillna(0)



    # Append the future dates DataFrame to the existing dataset
    apple_df = pd.concat([apple_df, future_dates_df], ignore_index=True)
    # Feature engineering
    apple_df = generate_features(apple_df)

    
    print(apple_df.info())
    print(apple_df.tail())

    # Scale numerical features
    apple_df = scale_data(apple_df, numerical_features)

    # Save the processed and feature engineered data to a new CSV file
    save_data(apple_df, output_file)

