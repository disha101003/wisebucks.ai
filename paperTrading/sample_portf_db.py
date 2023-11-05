-- Users Table
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    -- Other user fields
);

-- Watchlist Table
CREATE TABLE watchlist (
    watchlist_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    stock_symbol VARCHAR(10),
    -- Other watchlist fields
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Equities Table
CREATE TABLE equities (
    equity_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    stock_symbol VARCHAR(10),
    quantity INT,
    purchase_price DECIMAL(10, 2),
    -- Other equity fields
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Account Balance Table
CREATE TABLE account_balance (
    user_id INT PRIMARY KEY,
    balance DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Account Value History Table
CREATE TABLE account_value_history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    timestamp DATETIME,
    account_value DECIMAL(10, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
