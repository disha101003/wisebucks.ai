import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

#7DAY PREDICTION

start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
stock_symbol = input("Enter stock ticker symbol (e.g., GOOGL): ")
prev_days = int(input("Enter the number of previous days you want to predict with in each simulation: "))
num_simulations = int(input("Enter the number of simulations you want in Monte simulation: "))

# Retrieve historical data for the specified stock and user-defined dates
data = yf.download(stock_symbol, start=start_date, end=end_date)
days = len(data) # Number of days in the data
dt = 1 / days  # Time interval

np.random.seed(42)
actual_price = data['Close'].iloc[-1]

def monte_carlo_7_days(start_price, days, mu, sigma, prev_days):
    dt = 1 / days
    price = np.zeros(days + 7)
    price[0] = start_price

    for x in range(1, days + 8):
        total_shock = 0
        for i in range(prev_days):
            total_shock += np.random.normal(loc=mu, scale=sigma)
        shock = total_shock / prev_days
        drift = mu * dt

        if x < len(price):
            price[x] = price[x - 1] + (price[x - 1] * (drift + shock))

    return price[-7:]  # Return the next 7-day predictions

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

sim = np.zeros(num_simulations)
simulations = np.zeros((num_simulations, 7))

for i in range(num_simulations):
    start_price = data['Adj Close'].iloc[0]
    mu = data['Adj Close'].pct_change().mean()
    sigma = data['Adj Close'].pct_change().std()
    result = monte_carlo_7_days(start_price, days, mu, sigma, prev_days)

    sim[i] = result[-1]  # Store the final price
    simulations[i, :] = result  # Store the 7-day predictions

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

plt.show()

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


plt.show()

# Plot the median of the 7-day predictions
day_predicted_prices = np.median(simulations, axis=0)


plt.xlabel('Future Days from 10/05/2023')
plt.ylabel('Price ($)')
plt.title(f'Monte Carlo Analysis of {stock_symbol} with 7 day future-prices')

plt.plot(range(1, 8), day_predicted_prices, marker='o', label='Predicted Prices')

plt.show()


