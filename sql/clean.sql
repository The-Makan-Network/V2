DROP TABLE IF EXISTS allusers CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS sellers CASCADE;
DROP TABLE IF EXISTS buyers CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TRIGGER IF EXISTS update_sellers on products;
DROP TRIGGER IF EXISTS check_status on transactions;


/*
SELECT * FROM allusers;
SELECT * FROM products;
SELECT * FROM transactions;
SELECT * FROM reviews;
*/
