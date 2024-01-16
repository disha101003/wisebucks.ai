import yfinance as yf
import numpy as np
import pandas as pd
from monteCarlo import monte_carlo
from monteCarlo import stockAnalysis
import matplotlib.pyplot as plt


# Get user inputs
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
prev_days = int(input("Enter the number of previous days you want to predict with in each simulation: "))
num_simulations = int(input("Enter the number of simulations you want in Monte simulation: "))

# Get the list of S&P 500 tickers
sp500 = pd.read_excel("SP_500_Companies.xlsx")
sp500_tickers = sp500['Symbol'].tolist()



# sp500_tickers = yf.Tickers('^GSPC').tickers  # Fetch S&P 500 companies

# Initialize a list to store the final predictions
predictions_data = []

# monte carlo simulation for all 500 companies
for ticker in sp500_tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    if len(data) == 0:
        print(f"Warning: No data available for {ticker}. Skipping.")
        continue
    days = len(data)
    dt = 1 / days

    sim = np.zeros(num_simulations)
    for i in range(num_simulations):
        start_price = data['Close'].iloc[0]
        mu = data['Close'].pct_change().mean()
        sigma = data['Close'].pct_change().std()
        result = monte_carlo(start_price, days, mu, sigma, prev_days, dt)
        sim[i] = result[days - 1]

    predicted_price = np.median(np.sort(sim))

    predictions_data.append({'Symbol': ticker, 'Predicted Price': predicted_price})

    # plt.figure(figsize=(15, 8))
    # for i in range(num_simulations):
    #     plt.plot(result)

    #Following code to write each of the data into a .txt file

with open('predictions_data.txt', 'w') as file:
    file.write("Start Date: " + start_date)
    file.write("\nEnd Date: " + end_date)
    file.write("\nSimulations for each Monte Carlo " + str(num_simulations))
    file.write("\n\n")
    for prediction in predictions_data:
        file.write(f"Symbol: {prediction['Symbol']}, Predicted Price: {prediction['Predicted Price']}\n")

#uses pandas to create the dataframe in.xlsx file
# predictions_df = pd.DataFrame(predictions_data)
#
# predictions_df.to_excel('predictions.xlsx', index=False)

#TODO: need to store in a .txt file | also make sure to include accuracy rate