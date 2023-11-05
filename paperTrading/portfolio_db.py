-- Users table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    available_funds DECIMAL(15, 2) NOT NULL
);

//replace stocks table with new web scraping code
-- Stocks table (  
CREATE TABLE stocks (
    stock_id INT PRIMARY KEY AUTO_INCREMENT,
    symbol VARCHAR(10) NOT NULL,
    current_price DECIMAL(15, 2) NOT NULL
);

-- User stocks table to keep track of user's stocks
CREATE TABLE user_stocks (
    user_id INT,
    stock_id INT,
    quantity INT NOT NULL,
    average_price DECIMAL(15, 2) NOT NULL,
    PRIMARY KEY (user_id, stock_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);

-- Transactions table
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    stock_id INT NOT NULL,
    quantity INT NOT NULL, -- Positive for buy, negative for sell
    price_at_transaction DECIMAL(15, 2) NOT NULL,
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (stock_id) REFERENCES stocks(stock_id)
);

