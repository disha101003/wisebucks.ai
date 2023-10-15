import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# uses yfinance library to get the three stocks data for analysis
stocks = ["GOOGL", "AMZN", "TSLA"]
data = yf.download(stocks, start="2022-01-01", end="2023-01-01") #retrieves data for the 365 days
stock_returns = data['Adj Close'].pct_change().dropna()

days = 365
dt = 1 / days #time interval

#random seed for reproducibility
np.random.seed(42)

#Monte carlo simulation with four paramters
#start_price (initial stock price),
# days (number of simulation days),
# mu (average daily return of the stock),
# sigma (standard deviation of the stock’s daily returns)
def monte_carlo(start_price, days, mu, sigma):
    price = np.zeros(days)  # initializes price with zeros
    price[0] = start_price

    shock = np.zeros(days)  # initializes shock array
    drift = np.zeros(days)  # initializes drift array

    for x in range(1, days):
        shock[x] = np.random.normal(loc=mu * dt, scale=sigma * np.sqrt(dt))   #random shock for the current day is
        # generated using a normal distribution of paramters
        drift[x] = mu * dt  # expected change in price based on the average daily return and time interval

        price[x] = price[x - 1] + (price[x - 1] * (drift[x] + shock[x]))  # computed by applying the drift and
        # shock components to the previous day’s price and stores that in the price array
    return price

# Perform 1,000 Monte Carlo simulations for each stock
num_simulations = 1000

for idx, stock_symbol in enumerate(stocks): #this goes through each of the three stocks I analyze
    stock_data = data['Adj Close'][stock_symbol] #retrieves the adjusted closing prices of all the stocks in your datase
    # and indexes into the 'Adj Close' column to select the specific stock symbol
    start_price = stock_data.iloc[0] #retrieves initial element from stock_data Adj Close column
    mu = stock_returns[stock_symbol].mean() #mean of daily percentage values
    sigma = stock_returns[stock_symbol].std() #standard deviation of daily percentage values

    #following code segment plots monte carlo siulation
    plt.figure(figsize=(15, 8))
    # stores the simulation results in sim array that is initialized with 1000 zeros
    sim = np.zeros(num_simulations)
    for i in range(num_simulations): #goes through the thousand simulations that I set
        result = monte_carlo(start_price, days, mu, sigma)  #passed the initial stock price,
        # the number of days for the simulation, and Tesla-specific average daily return and
        # standard deviation of daily returns
        sim[i] = result[days - 1] #final price is stored
        plt.plot(result)
    #sets axes and title for Graph #1
    plt.xlabel('Days')
    plt.ylabel('Price')
    plt.title(f'Monte Carlo Simulations for {stock_symbol}')

    # plotting histogram
    plt.figure(figsize=(10, 7)) # creates a new figure for the plot with dimensions 10 inches by 7 inches
    plt.hist(sim, bins=100) #generates a histogram plot using the data from the sim array.
    # the sim array contains the simulated final prices of each of the stocks
    plt.figtext(0.6, 0.7, "Mean: {:.2f}\nStd: {:.2f}\nStart Price: {:.2f}".format(sim.mean(), sim.std(), start_price))
    #adds text annotations to the figure at specific coordinates. It displays the mean, standard deviation, and start price of the simulated prices

    plt.title(f'Histogram for Monte Carlo Simulations of {stock_symbol}')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.show()

