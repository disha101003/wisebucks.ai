DELIMITER //

CREATE PROCEDURE SellStock(IN user_id INT, IN stock_id INT, IN sell_quantity INT, IN stock_price DECIMAL(15,2))
BEGIN
    DECLARE owned_quantity INT;

    -- Check if user owns enough stocks
    SELECT quantity INTO owned_quantity FROM user_stocks WHERE user_id = user_id AND stock_id = stock_id;
    IF owned_quantity < sell_quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock quantity';
    END IF;

    -- Remove the stocks from the user's portfolio
    UPDATE user_stocks SET quantity = quantity - sell_quantity WHERE user_id = user_id AND stock_id = stock_id;

    -- Add the funds to the user's balance
    UPDATE users SET available_funds = available_funds + (sell_quantity * stock_price) WHERE user_id = user_id;

    -- Record the transaction
    INSERT INTO transactions (user_id, stock_id, quantity, price_at_transaction)
    VALUES (user_id, stock_id, -sell_quantity, stock_price);
END //

DELIMITER ;
