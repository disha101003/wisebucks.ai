import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import sqlalchemy as db
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.models import load_model as keras_load_model  # Rename the imported function
import matplotlib.pyplot as plt
from keras.initializers import GlorotUniform
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Activation
from keras import optimizers
from keras.callbacks import ModelCheckpoint, EarlyStopping
import joblib

def load_data(file_path, symbol): 
    """
    Load the data for a given company (symbol) from the database

    :param file_path: str: The path to the database file (atradebot.db)
    :return: pd.DataFrame: The data for the given company
    """


    # connect to the database
    engine = db.create_engine(f'sqlite:///{file_path}', echo=True)
    connection = engine.connect()

    # fetch the data
    query = "SELECT * FROM stocks WHERE symbol = '{}'".format(symbol)
    data = pd.read_sql(query, connection)
    return data 


def preprocess_data(df):
    """
    Preprocess company data for training the LSTM model

    :param df: pd.DataFrame: The company data
    :return: np.array: The scaled features, 
             np.array: The scaled target variable, 
             np.array: The scaled dataset (features + target variable)
    """

    # Define the features and target variables
    target = ['TargetNextClose']
    symbol = df['symbol'].unique()[0] # Get the symbol name

    df.dropna(subset=['RSI', 'EMAF', 'EMAM', 'EMAS'], inplace=True)

    print(df)

    features = df.drop(['symbol', 'close', 'date', 'quarter', 'volume', 'daily_range', 'daily_return', 'high', 'low'], axis=1).columns.tolist() # list

    X = df[features].values
    y = df[target].values

    y_scaler = MinMaxScaler(feature_range=(0, 1))
    y_scaled = y_scaler.fit_transform(y)

    # Save the target variable scaler for this symbol
    y_scaler_filename = f"/Users/anujthakkar/Documents/Purdue/Projects/wisebucks.ai/LSTM/scalers/{symbol}_y_scaler.save"
    joblib.dump(y_scaler, y_scaler_filename)

    # Apply scaling to the features 'X'
    x_scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = x_scaler.fit_transform(X)

    # Save the feature scaler for this symbol
    x_scaler_filename = f"/Users/anujthakkar/Documents/Purdue/Projects/wisebucks.ai/LSTM/scalers/{symbol}_x_scaler.save"
    joblib.dump(x_scaler, x_scaler_filename)

    data_set_scaled = np.concatenate((X_scaled, y_scaled), axis=1)

    return X_scaled, y_scaled, data_set_scaled



def prepare_lstm_input(data_set_scaled, backcandles):
    """
    Prepare the input for the LSTM model

    :param data_set_scaled: np.array: The scaled dataset (features + target variable)
    :param backcandles: int: The number of previous candles to consider
    :return: np.array: The input for the LSTM model, shaped as (num_samples, backcandles, num_features)
             np.array: The target variable for the LSTM model
    """


    # multiple feature from data provided to the model
    X = []

    print(data_set_scaled.shape[0])
    for j in range(8):#data_set_scaled[0].size):#2 columns are target not X
        X.append([])
        for i in range(backcandles, data_set_scaled.shape[0]):#backcandles+2
            X[j].append(data_set_scaled[i-backcandles:i, j])

    X=np.moveaxis(X, [0], [2]) #move axis from 0 to position 2

    X, yi =np.array(X), np.array(data_set_scaled[backcandles:,-1])
    y=np.reshape(yi,(len(yi),1))

    print(f'X shape: {X.shape}')
    print(f'y shape: {y.shape}')

    return X, y

def split_data(X, y, test_size, backcandles):
    """
    Split the data into training and testing

    :param X: np.array: The input for the LSTM model
    :param y: np.array: The target variable for the LSTM model
    :param test_size: float: The proportion of the dataset to include in the test split
    :param backcandles: int: The number of previous candles to consider
    :return: np.array: The input for the LSTM model (training set)

    """


    # Split the data into training and testing
    splitlimit = int((1-test_size)*len(X))
    X_train, X_test = X[:splitlimit], X[splitlimit:]
    y_train, y_test = y[:splitlimit], y[splitlimit:]
    print(f'X_train shape: {X_train.shape}'
            f' X_test shape: {X_test.shape}')
    print(f'y_train shape: {y_train.shape}'
            f' y_test shape: {y_test.shape}')

    return X_train, X_test, y_train, y_test, splitlimit, backcandles

def build_lstm_model(input_shape, X_train, y_train):
    """
    Build an LSTM model

    :param input_shape: tuple: The shape of the input for the LSTM model
    :param X_train: np.array: The input for the LSTM model
    :param y_train: np.array: The target variable for the LSTM model
    :return: keras.Model: The LSTM model
    """
    model = Sequential()
    # must set return_sequence to False for last LSTM layer
    model.add(LSTM(100, input_shape=input_shape, activation='tanh', return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(units=100,return_sequences=True))
    model.add(Dropout(0.4))
    model.add(LSTM(units=50,return_sequences=False))
    model.add(Dropout(0.05))
    model.add(Dense(1, activation='relu'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x=X_train, y=y_train, batch_size=10, epochs=50, validation_split = 0.1)
    return model

if __name__ == "__main__":

    data_file_path = '/Users/anujthakkar/Documents/Purdue/Projects/wisebucks.ai/data/atradebot.db'

    epochs = 100
    batch_size = 5 
    backcandles = 6

    model_output_text_file = '/Users/anujthakkar/Documents/Purdue/Projects/wisebucks.ai/LSTM/outputs/newModelOutput.txt'

    # Get the list of stock symbols from the CSV
    stock_df = pd.read_csv('data/sp-500-index-10-29-2023.csv')
    symbols = stock_df['Symbol'].tolist()[0:2]

    for symbol in symbols:
        data_frame = load_data(data_file_path, symbol).drop(['id'], axis=1)
        dates = data_frame['date']

        X_scaled, y_scaled, data_set_scaled = preprocess_data(data_frame)

        X_lstm, y_lstm = prepare_lstm_input(data_set_scaled, backcandles)
        X_train, X_test, y_train, y_test, splitlimit, backcandles = split_data(X_lstm, y_lstm, test_size=0.1, backcandles=backcandles)
        dates_in_test = dates[splitlimit+backcandles:]

        model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]), X_train=X_train, y_train=y_train)

        y_pred = model.predict(X_test)

        y_scaler_filename = f"/Users/anujthakkar/Documents/Purdue/Projects/wisebucks.ai/LSTM/scalers/{symbol}_y_scaler.save"
        x_scaler_filename = f"/Users/anujthakkar/Documents/Purdue/Projects/wisebucks.ai/LSTM/scalers/{symbol}_x_scaler.save"

        # load y_scaler and x_scaler given symbol
        y_scaler = joblib.load(y_scaler_filename)
        x_scaler = joblib.load(x_scaler_filename)

        # inverse transform the predictions
        y_pred = y_scaler.inverse_transform(y_pred)
        y_test = y_scaler.inverse_transform(y_test)

        

        for i in range(len(y_pred)):    
            # get the value of the date from dates
            print(dates_in_test.iloc[i], y_pred[i], y_test[i])
