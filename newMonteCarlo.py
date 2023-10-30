import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
stock_symbol = input("Enter stock ticker symbol (e.g., GOOGL): ")
prev_days = int(input("Enter the number of previous days you want to predict with in each simulation: "))
num_simulations = 30

data = yf.download(stock_symbol, start=start_date, end=end_date)
days = len(data)
dt = 1 / days

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

    return price # compare all these prices curve and get accuracies for all of these prices

# accuracies to be plotted
def accuracies(start_price, days, mu, sigma, prev_days):
    price = np.zeros(days)  # initializes prices with 0
    price[0] = start_price
    accuracies = []

    for x in range(1, days):
        total_shock = 0
        for day in range(prev_days):
            total_shock += np.random.normal(loc=mu, scale=sigma)  # Accumulate shocks from previous days
        shock = total_shock / prev_days  # Average shock from previous days
        drift = mu * dt

        # computed by applying the drift and shock components to the previous day’s price and stores that in the price array
        price[x] = price[x - 1] + (price[x - 1] * (drift + shock))

        # Calculate accuracy for the current day and store it
        predicted_price = price[x]
        actual_price = data['Close'].iloc[x]  # Actual price for the current day
        accuracy = (1 - abs(actual_price - predicted_price) / actual_price) * 100
        accuracies.append(accuracy)

    return accuracies

# Perform Monte Carlo simulations for the specified stock for 30 days
sim = np.zeros((num_simulations, days))
for i in range(num_simulations):
    start_price = data['Adj Close'].iloc[0] # retrieves the adjusted closing prices of all the stocks in your dataset
    # and indexes into the 'Adj Close' column to select the specific stock symbol
    mu = data['Adj Close'].pct_change().mean() # mean of daily percentage values entire year
    sigma = data['Adj Close'].pct_change().std()   # standard deviation of daily percentage values

    result = monte_carlo(start_price, days, mu, sigma)
    sim[i] = result  # store the simulation results

# Plotting Monte Carlo simulations for each day
plt.figure(figsize=(15, 8))
for i in range(num_simulations):
    plt.plot(sim[i])

# Print predicted prices and accuracies
for i in range(num_simulations):
    predicted_price = sim[i][-1]
    accuracy = (1 - abs(actual_price - predicted_price) / actual_price) * 100
    print(f"Predicted price for day {i}: ${predicted_price:.2f} | Accuracy: {accuracy:.2f}%")

# Perform Monte Carlo simulation to get accuracies for each day
accuracies_per_day = accuracies(data['Close'].iloc[0], days, data['Close'].pct_change().mean(),
                                data['Close'].pct_change().std(), prev_days)

plt.figure(figsize=(12, 6))
plt.plot(range(1, days), accuracies_per_day, color='b', linewidth=1)
plt.xlabel('Day')
plt.ylabel('Accuracy (Decimal)')
plt.title(f'Accuracy of {stock_symbol} Predictions from {start_date} to {end_date}')
plt.tight_layout()

for i in range(num_simulations):
    plt.figure(figsize=(10, 7))
    plt.hist(sim[:, i], bins=100)
    plt.figtext(0.6, 0.7, f"Mean: {sim[:, i].mean():.2f}\nStd: {sim[:, i].std():.2f}\nStart Price: {start_price:.2f}")
    plt.title(f'Histogram for Monte Carlo Simulations of {stock_symbol} on Day {i}')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.savefig(f'histogram_day_{i}.png')  # Save the histogram to a file
    plt.close()

# Show plots
plt.show()
