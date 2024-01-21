import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sqlalchemy as db
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.models import load_model  # Rename the imported function
from train_LSTM import *
import joblib


# Load data
def load_data(file_path, symbol):
    # connect to the database
    engine = db.create_engine(f'sqlite:///{file_path}', echo=True)
    connection = engine.connect()

    # fetch the data
    query = "SELECT * FROM stocks WHERE symbol = '{}'".format(symbol)
    data = pd.read_sql(query, connection)

    return data


if __name__ == "__main__":
        
    data_file_path = 'data/atradebot.db'
    epochs = 100
    batch_size = 5

    # Get the list of stock symbols from the CSV
    stock_df = pd.read_csv('data/sp-500-index-10-29-2023.csv')
    #symbols = stock_df['Symbol'].tolist()
    symbols = ['MSFT'] # to test with a few symbols
    
    dict_of_predictions = {}

    for symbol in symbols:


        model_path = f'./LSTM/models/{symbol}_lstm_model.h5'
        
        data_frame = load_data(data_file_path, symbol).drop(['id'], axis=1)

        X_scaled, y_scaled = preprocess_data(data_frame) # drops ['symbol', 'close', 'date', 'quarter']
        X_lstm = prepare_lstm_input(X_scaled)

        # Predict
        # Load the trained LSTM model
        model = load_model(f'./LSTM/models/{symbol}_lstm_model.h5')

        # Get the last available data point for prediction
        last_data_point = X_lstm[-1:]
        last_data_point_date = data_frame.iloc[-1]['date']
        print(f"Symbol: {symbol}, Last Data Point Date: {last_data_point_date}")

        # Make a prediction for the next day's Close price
        predicted_scaled_close = model.predict(last_data_point)
        # print(f"PREDICTED SCALED CLOSE: {predicted_scaled_close}")

        # Load the scaler used for training
        scaler_filename = f"./LSTM/scalers/{symbol}_y_scaler.save"
        scaler = joblib.load(scaler_filename)

        # Reuse the same scaler used for scaling during training
        predicted_close = scaler.inverse_transform(predicted_scaled_close)
        print(f"PREDICTED CLOSE: {predicted_close[0][0]}")

        # Get the actual Close price for the next day
        date = data_frame.iloc[-1]['date']
        open_price = most_recent_open(data_frame)
        actual_close = data_frame.iloc[-1]['close']
        print(f"ACTUAL CLOSE: {actual_close}")
        high_price = most_recent_high(data_frame)
        low_price = most_recent_low(data_frame)
        volume = most_recent_volume(data_frame)
        volatility = most_recent_volatility(data_frame)

        key = (symbol, date)
        values = [open_price, actual_close, high_price, low_price, volume, volatility, predicted_close[0][0]]

        print(f"Percent error for {symbol}: {abs((actual_close - predicted_close[0][0]) / actual_close) * 100}")

        dict_of_predictions[key] = values

        import matplotlib.pyplot as plt
        # Get the most recent 100 days from the training data
        recent_dates = data_frame.iloc[-100:]['date']

        # Get the close prices for the most recent 100 days from the training data
        recent_close_prices = data_frame.iloc[-100:]['close']

        # Get all the dates from the testing data
        testing_dates = data_frame.iloc[X_train.shape[0]:]['date']

        # Get the close prices for the testing data
        testing_close_prices = data_frame.iloc[X_train.shape[0]:]['close']

        # get prediction for all the testing dates
        predicted_close = model.predict(X_test)

        # Reuse the same scaler used for scaling during training
        predicted_close = scaler.inverse_transform(predicted_close)

        """"
        # Plot the graph
        plt.plot(recent_dates, recent_close_prices, label='Actual Close Price (Training Data)')
        plt.plot(testing_dates, testing_close_prices, label='Actual Close Price (Testing Data)')
        plt.plot(testing_dates, predicted_close, label='Predicted Close on Testing Data')
        plt.xlabel('Dates')
        plt.ylabel('Close Price')
        plt.title('Close Price vs Dates')
        plt.legend()
        plt.savefig(f'./LSTM/outputs/{symbol}_close_price.png')
        # clear the figure
        plt.clf()
        """