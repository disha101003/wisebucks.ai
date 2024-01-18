import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#other things to-do
#Monte carlo simulation with four paramters
#start_price (initial stock price),
# days (number of simulation days),
# mu (average daily return of the stock),
# sigma (standard deviation of the stock’s daily returns)

#TO-DO for the next year: compare from previous year to next year
#change the value from one day to one month
#take data for all S&P 500

# uses yfinance library to get the stocks for analysis based on user inputs
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
stock_symbol = input("Enter stock ticker symbol (e.g., GOOGL): ")
prev_days = int(input("Enter the number of previous days you want to predict with in each simulation: "))
num_simulations = int(input("Enter the number of simulations you want in Monte simulation: "))

# Retrieve historical data for the specified stock and user-defined dates
data = yf.download(stock_symbol, start=start_date, end=end_date)
days = len(data)  # Number of days in the data
dt = 1 / days  # Time interval

# Random seed for reproducibility
np.random.seed(42)
actual_price = data['Close'].iloc[-1]

def monte_carlo(start_price, days, mu, sigma):
    price = np.zeros(days)  # Initializes price with zeros
    price[0] = start_price

    for x in range(1, days):
        total_shock = 0
        for day in range(prev_days):
            total_shock += np.random.normal(loc=mu, scale=sigma)  # Accumulate shocks from previous days
        shock = total_shock / prev_days  # Average shock from previous days
        drift = mu * dt  # Expected change in price based on the average daily return

        # computed by applying the drift and shock components to the previous day’s price and stores that in the price array
        price[x] = price[x - 1] + (price[x - 1] * (drift + shock))

    return price #compare all these prices curve and get accuracies for all of these prices

#new accuracy method
def accur(start_date, end_date, days, mu, sigma, start_price, prev_days):
    price = np.zeros(days)  # initializes prices with 0
    price[0] = start_price
    accuracies = []

    print('hello')

def accuracies(start_price, days, mu, sigma, prev_days):
    dt = 1 / days
    price = np.zeros(days)
    price[0] = start_price
    accuracies = []

    for x in range(1, days):
        total_shock = 0
        for day in range(days):
            total_shock += np.random.normal(loc=mu, scale=sigma)
        shock = total_shock / days
        drift = mu * dt

        price[x] = price[x - 1] + (price[x - 1] * (drift + shock))

        predicted_price = price[x]
        accuracy = (1 - abs(actual_price - predicted_price) / actual_price) * 100
        accuracies.append(accuracy)

    return accuracies

#accuracies to be plotted
# def accuracies(start_price, days, mu, sigma, prev_days):
#     price = np.zeros(days)  # initializes prices with 0
#     price[0] = start_price
#     accuracies = []
#
#     for x in range(1, days):
#         total_shock = 0
#         for day in range(prev_days):
#             total_shock += np.random.normal(loc=mu, scale=sigma)  # Accumulate shocks from previous days
#         shock = total_shock / prev_days  # Average shock from previous days
#         drift = mu * dt  # Expected change in price based on the average daily return
#
#         # computed by applying the drift and shock components to the previous day’s price and stores that in the price array
#         price[x] = price[x - 1] + (price[x - 1] * (drift + shock))
#
#         # Calculate accuracy for the current day and store it
#         predicted_price = price[x]
#         actual_price = data['Close'].iloc[x]  # Actual price for the current day
#         accuracy = (1 - abs(actual_price - predicted_price) / actual_price) * 100
#         accuracies.append(accuracy)
#
#     return accuracies

# Perform x amount of Monte Carlo simulations for the specified stock
sim = np.zeros(num_simulations)
plt.figure(figsize=(15, 8))
for i in range(num_simulations):
    start_price = data['Adj Close'].iloc[0] #retrieves the adjusted closing prices of all the stocks in your datase
    # and indexes into the 'Adj Close' column to select the specific stock symbole
    mu = data['Adj Close'].pct_change().mean() #mean of daily percentage values entire year
    sigma = data['Adj Close'].pct_change().std()   #standard deviation of daily percentage values

    result = monte_carlo(start_price, days, mu, sigma)
    sim[i] = result[days-1]  # final price is stored
    plt.plot(result)

#prints out predicted price for next day and accuracy of that value compared to actual data
predicted_price = np.median(np.sort(sim))
print("Predicted price for the next day after " + end_date + f" is ${predicted_price:.2f}")
accuracy = (1- abs(actual_price - predicted_price) / actual_price) * 100
print("Accuracy: {:.2f}%".format(accuracy))

# sets axes and title for Graph #1
plt.xlabel('Days')
plt.ylabel('Price')
plt.title(f'Monte Carlo Simulation for {stock_symbol}')

# Perform Monte Carlo simulation to get accuracies for each day
accuracies_per_day = accuracies(data['Close'].iloc[0], days, data['Close'].pct_change().mean(),
                                  data['Close'].pct_change().std(), prev_days)

# Plotting accuracies for each day
plt.figure(figsize=(12, 6))
plt.plot(data.index[1:], accuracies_per_day, color='b', linewidth=1)
plt.xlabel('Date')
plt.ylabel('Accuracy (Decimal)')
plt.title(f'Accuracy of {stock_symbol} Predictions from {start_date} to {end_date}')
plt.xticks(rotation=45)
plt.tight_layout()

# Plot histogram
plt.figure(figsize=(10, 7))  #generates a histogram plot using the data from the sim array.
    # the sim array contains the simulated final prices of each of the stocks
plt.hist(sim, bins=100)
plt.figtext(0.6, 0.7, "Mean: {:.2f}\nStd: {:.2f}\nStart Price: {:.2f}".format(sim.mean(), sim.std(), start_price))
# adds text annotations to the figure at specific coordinates. It displays the mean, standard deviation, and start price of the simulated prices
plt.title(f'Histogram for Monte Carlo Simulations of {stock_symbol}')
plt.xlabel('Price')
plt.ylabel('Frequency')


#write next graph here

# Initialize lists to store accuracies and predicted prices
accuracies_list = []
predicted_prices_list = []

arr = []

# Iterate through the range from -30 to 30 days
# Think about price your predicting, if oprice goes up as well, otherwise consider a failure.
# where the error builds o
# if you make current predicition to next day
# quantize our final score
# need an alogiirhtm to combine all the tests
# if it is  anegative prediction, you do minus
# quantizing --> if predicting score is more (that way you factor + (predicited)/(actual)
# if you get a 60% movement accuracy better than S&P 500
for prev_days in range(-30, 30):  #-30, 30 Predict whether it goes up or down
    shifted_start_date = pd.to_datetime(start_date) + pd.DateOffset(days=prev_days)
    shifted_end_date = pd.to_datetime(end_date) + pd.DateOffset(days=prev_days)

    days = len(data)
    dt = 1 / days

    start_price = data['Close'].iloc[0]
    mu = data['Close'].pct_change().mean()
    sigma = data['Close'].pct_change().std()

    accuracy_values = accuracies(start_price, days, mu, sigma, prev_days)
    arr.extend(accuracy_values)

    mean_accuracy = np.mean(arr)
    accuracies_list.append(mean_accuracy)
    predicted_prices_list.append(prev_days)


plt.figure(figsize=(10, 6))
plt.plot(predicted_prices_list, accuracies_list, marker='o', linestyle='-', color='b')
plt.xlabel('Days Shifted')
plt.ylabel('Accuracy (%)')
plt.title('Accuracy of Predictions vs. Days Shifted')
plt.grid(True)

plt.show()

def main():
    # Your main code goes here
    print("This is the main method.")

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Call the main method
    main()
