import numpy as np
import matplotlib.pyplot as plt

def calculate_portfolio_performance(weights, returns, cov_matrix):
    portfolio_return = np.dot(weights, returns)
    portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_return, portfolio_stddev

def monte_carlo_simulation(returns, cov_matrix, num_portfolios):
    portfolio_returns = []
    portfolio_stddevs = []
    for _ in range(num_portfolios):
        weights = np.random.random(len(returns))
        weights /= np.sum(weights)
        portfolio_return, portfolio_stddev = calculate_portfolio_performance(weights, returns, cov_matrix)
        portfolio_returns.append(portfolio_return)
        portfolio_stddevs.append(portfolio_stddev)
    return np.array(portfolio_returns), np.array(portfolio_stddevs)

stock_returns = np.array([0.1, 0.05])
cov_matrix = np.array([[0.0004, 0.0002], [0.0002, 0.0003]])

#simulation amount
num_portfolios = 10000

# Monte Carlo simulation
portfolio_returns, portfolio_stddevs = monte_carlo_simulation(stock_returns, cov_matrix, num_portfolios)

# Plot results
plt.figure(figsize=(12, 6))
plt.scatter(portfolio_stddevs, portfolio_returns, c=portfolio_returns / portfolio_stddevs, marker='o', cmap='YlGnBu')
plt.title('Monte Carlo Simulation - Risk/Return Trade-off')
plt.xlabel('Portfolio Standard Deviation')
plt.ylabel('Portfolio Expected Return')
plt.colorbar(label='Sharpe Ratio')
plt.show()
