create database Mydb
use Mydb;
CREATE TABLE sales (
    sale_id INTEGER,
    customer TEXT,
    city TEXT,
    product TEXT,
    amount INTEGER,
    status TEXT
);
INSERT INTO sales VALUES
(1, 'Rahul', 'Bangalore', 'Laptop', 55000, 'Completed'),
(2, 'Priya', 'Mumbai', 'Mobile', 20000, 'Completed'),
(3, 'Amit', 'Dharwad', 'Headphones', 1500, 'Pending'),
(4, 'Sneha', 'Pune', 'Laptop', 60000, 'Completed'),
(5, 'Kiran', 'Hubli', 'Mouse', 500, 'Pending'),
(6, 'Ravi', 'Bangalore', 'Mobile', 18000, 'Completed'),
(7, 'Anjali', 'Chennai', 'Keyboard', 2500, 'Cancelled'),
(8, 'Arun', 'Dharwad', 'Laptop', 45000, 'Completed'),
(9, 'Neha', 'Mumbai', 'Mouse', 800, 'Pending'),
(10, 'Suresh', 'Hubli', 'Mobile', 22000, 'Completed');
select * from sales;

select customer, city from sales;
select * from sales where amount > 20000;
select * from sales where status = 'Completed';
select * from  sales where city = 'Bangalore' OR city = 'Mumbai';
select * from sales where NOT status = 'Completed';
select * from sales where customer LIKE 'A%';
select * from sales where city IN ('Bangalore', 'Mumbai', 'Dharwad');
select * from sales where amount BETWEEN 1000 AND 30000;
select * from sales where city IS NULL;

