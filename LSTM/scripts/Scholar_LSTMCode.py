"""
this file is used on Scholar cluster to train the model
Author: Anuj Thakkar

"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import sqlalchemy as db
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.models import load_model as keras_load_model  # Rename the imported function
import time
import matplotlib.pyplot as plt


# Load data
def load_data(file_path, symbol):
    # connect to the database
    engine = db.create_engine(f'sqlite:///{file_path}', echo=True)
    connection = engine.connect()

    # fetch the data
    query = "SELECT * FROM stocks WHERE symbol = '{}'".format(symbol)
    data = pd.read_sql(query, connection)

    return data

def most_reecent_date(df):
    return df.iloc[-1]['date']

def most_recent_open(df):
    return df.iloc[-1]['open']

def most_recent_close(df):
    return df.iloc[-1]['close']

def most_recent_high(df):
    return df.iloc[-1]['high']

def most_recent_low(df):
    return df.iloc[-1]['low']

def most_recent_volume(df):
    return df.iloc[-1]['volume']

def most_recent_volatility(df):
    return df.iloc[-1]['volatility']


def preprocess_data(df):
    import joblib

    # Define the features and target variables
    target = ['close']
    symbol = df['symbol'].unique()[0] # Get the symbol name
    features = df.drop(['symbol', 'close', 'date', 'quarter', 'volatility'], axis=1).columns.tolist()

    # Create arrays for the features and the response variable
    X = df[features].values
    y = df[target].values

    # Apply scaling to the target variable 'y' (Close prices)
    y_scaler = StandardScaler()
    y_scaled = y_scaler.fit_transform(y)

    # Save the target variable scaler for this symbol
    y_scaler_filename = f'/home/atthakka/wisebucks/LSTM/scalers/{symbol}_y_scaler.save'
    joblib.dump(y_scaler, y_scaler_filename)

    # Apply scaling to the features 'X'
    x_scaler = StandardScaler()
    X_scaled = x_scaler.fit_transform(X)

    # Save the feature scaler for this symbol
    x_scaler_filename = f'/home/atthakka/wisebucks/LSTM/scalers/{symbol}_x_scaler.save'
    joblib.dump(x_scaler, x_scaler_filename)

    return X_scaled, y_scaled

def prepare_lstm_input(X):

    time_steps = 1
    batch_size = X.shape[0]  # Get the number of samples in the batch
    X_lstm = X.reshape(batch_size, time_steps, X.shape[1])
    X_lstm = X_lstm.astype('float32')

    return X_lstm

def build_lstm_model(input_shape):
    model = Sequential()
    # must set return_sequence to False for last LSTM layer
    model.add(LSTM(100, input_shape=input_shape, activation='tanh', return_sequences=True))
    model.add(Dropout(0.05))
    model.add(LSTM(units=100,return_sequences=True))
    model.add(Dropout(0.4))
    model.add(LSTM(units=100,return_sequences=False))
    model.add(Dropout(0.05))
    model.add(Dense(1, activation='relu'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def train_lstm_model(model, X_train, y_train, epochs, batch_size):
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1, shuffle=False)
    return history

def print_model_summary(model):
    print(model.summary())

def load_model(model_path):
    model = keras_load_model(model_path)  # Use the imported Keras function
    return model


if __name__ == "__main__":

    model_output_text_file = '/home/atthakka/wisebucks/LSTM/outputs/model_output.txt'

    data_file_path = '/home/atthakka/wisebucks/data/atradebot.db'
    epochs = 100
    batch_size = 5

    # Get the list of stock symbols from the CSV
    stock_df = pd.read_csv('/home/atthakka/wisebucks/data/sp-500-index-10-29-2023.csv')
    print(len(stock_df))
    symbols = stock_df['Symbol'].tolist()
    symbols = symbols[61:250]
    #symbols = ['AAPL', 'AMZN', 'TSLA', 'GOOG', 'LULU', 'MSFT'] # to test with a few symbols
    

    dict_of_predictions = {}
    with open(model_output_text_file, 'a') as output_file:

        for symbol in symbols:
            
            
            model_path = f'/home/atthakka/wisebucks/LSTM/models/{symbol}_lstm_model.h5'

            data_frame = load_data(data_file_path, symbol).drop(['id'], axis=1)


            X_scaled, y_scaled = preprocess_data(data_frame) # drops ['symbol', 'close', 'date', 'quarter']
            X_lstm = prepare_lstm_input(X_scaled)

            X_train, X_test, y_train, y_test = train_test_split(X_lstm, y_scaled, test_size=0.01, shuffle=False)

            model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
            start_time = time.time()
            history = train_lstm_model(model, X_train, y_train, epochs=epochs, batch_size=batch_size)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print("Training time for {}: {:.2f} seconds".format(symbol, elapsed_time))

            # print model accuracy
            test_score = model.evaluate(X_test, y_test, verbose=0)
            print('Test Score: %.2f MSE (%.2f RMSE)' % (test_score, np.sqrt(test_score)))

            # Save the trained model
            model.save(f'/home/atthakka/wisebucks/LSTM/models/{symbol}_lstm_model.h5')

            # Predict
            # Load the trained LSTM model
            model = load_model(f'/home/atthakka/wisebucks/LSTM/models/{symbol}_lstm_model.h5')

            # Get the last available data point for prediction
            last_data_point = X_lstm[-1:]
            last_data_point_date = data_frame.iloc[-1]['date']
            print(f"Symbol: {symbol}, Last Data Point Date: {last_data_point_date}")

            # Make a prediction for the next day's Close price
            predicted_scaled_close = model.predict(last_data_point)
            # print(f"PREDICTED SCALED CLOSE: {predicted_scaled_close}")

            # Load the scaler used for training
            import joblib
            scaler_filename = f'/home/atthakka/wisebucks/LSTM/scalers/{symbol}_y_scaler.save'
            scaler = joblib.load(scaler_filename)

            # Reuse the same scaler used for scaling during training
            predicted_close = scaler.inverse_transform(predicted_scaled_close)
            print(f"PREDICTED CLOSE: {predicted_close[0][0]}")

            # Get the actual Close price for the next day
            date = data_frame.iloc[-1]['date']
            open_price = most_recent_open(data_frame)
            print(f"OPEN PRICE: {open_price}")
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
            print(dict_of_predictions)
            
            # Write output to the text file
            print("now writing output")
            output_file.write("Symbol: " + symbol + " Date: " + last_data_point_date + "\n")
            output_file.write(f"Actual Close Price: {actual_close:.2f}\n")
            output_file.write(f"LSTM Predicted Close Price: {predicted_close[0][0]:.2f}\n")
            output_file.write(f"Percent Error: {abs((actual_close - predicted_close[0][0]) / actual_close) * 100:.2f}%\n")
            output_file.write("Test Score: %.2f MSE (%.2f RMSE)" % (test_score, np.sqrt(test_score)))
            output_file.write("\n")
            output_file.write("\n")
            print("finished output")
            
