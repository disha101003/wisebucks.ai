DELIMITER ///

CREATE PROCEDURE BuyStock(IN user_id INT, IN stock_id INT, IN buy_quantity INT, IN stock_price DECIMAL(15,2))
BEGIN
    DECLARE funds DECIMAL(15,2);
    DECLARE total_cost DECIMAL(15,2);

    -- Calculate total cost of purchase
    SET total_cost = buy_quantity * stock_price;

    -- Check if user has enough funds
    SELECT available_funds INTO funds FROM users WHERE user_id = user_id;
    IF funds < total_cost THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient funds';
    END IF;

    -- Deduct the total cost from the user's funds
    UPDATE users SET available_funds = available_funds - total_cost WHERE user_id = user_id;

    -- Add the stocks to the user's portfolio
    INSERT INTO user_stocks (user_id, stock_id, quantity, average_price)
    VALUES (user_id, stock_id, buy_quantity, stock_price)
    ON DUPLICATE KEY UPDATE
        quantity = quantity + buy_quantity,
        average_price = (average_price * quantity + stock_price * buy_quantity) / (quantity + buy_quantity);

    -- Record the transaction
    INSERT INTO transactions (user_id, stock_id, quantity, price_at_transaction)
    VALUES (user_id, stock_id, buy_quantity, stock_price);
END //

DELIMITER ;
