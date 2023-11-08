import numpy as np
import pandas as pd
import sqlalchemy as db
from keras.models import load_model as keras_load_model  # Rename the imported function

# Load model
def load_custom_model(model_path):
    model = keras_load_model(model_path)  # Use the imported Keras function
    return model

# Load data
def load_data(file_path, symbol):
    # connect to the database
    engine = db.create_engine(f'sqlite:///{file_path}', echo=True)
    connection = engine.connect()

    # fetch the data
    query = "SELECT * FROM stocks WHERE symbol = '{}'".format(symbol)
    data = pd.read_sql(query, connection)

    return data

# Preprocess data
def preprocess_data(df):
    # Define the features and target variables
    target = ['close']
    features = df.drop(['symbol','close', 'date', 'quarter'], axis=1).columns.tolist()

    # Create arrays for the features and the response variable
    X = df[features].values
    y = df[target].values

    return X, y

# Prepare LSTM input
def prepare_lstm_input(X):
    time_steps = 1
    batch_size = X.shape[0]  # Get the number of samples in the batch
    X_lstm = X.reshape(batch_size, time_steps, X.shape[1])
    X_lstm = X_lstm.astype('float32')
    print(f'X_lstm shape: {X_lstm.shape}')

    return X_lstm

# Predict
def predict(model, X_test):
    y_pred = model.predict(X_test)
    return y_pred

# Evaluate
def evaluate(y_test, y_pred):
    rmse = np.sqrt(np.mean((y_test - y_pred)**2))
    return rmse

if __name__ == "__main__":

    # predict for each symbol in the LSTM/models directory
    symbols = ['AAPL', 'AMZN', 'GOOG', 'TSLA']

    for symbol in symbols:

        # load model
        model_path = f'LSTM/models/{symbol}_lstm_model.h5'
        model = load_custom_model(model_path)

        # load data
        file_path = './atradebot.db'
        df = load_data(file_path, symbol)

        # preprocess data
        X, y = preprocess_data(df)

        # prepare LSTM input
        X_lstm = prepare_lstm_input(X)

        # predict
        y_pred = predict(model, X_lstm)
        print(f'{symbol} y_pred: {y_pred}')

        # evaluate
        rmse = evaluate(y, y_pred)
        print(f'{symbol} RMSE: {rmse}')

