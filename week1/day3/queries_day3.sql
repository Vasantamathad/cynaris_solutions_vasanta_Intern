create database day3;
use day3;
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    sale_date DATE,
    region VARCHAR(50),
    city VARCHAR(50),
    category VARCHAR(50),
    product VARCHAR(100),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);
INSERT INTO sales
(sale_id, sale_date, region, city, category, product, quantity, unit_price, total_amount)
VALUES
(1, '2026-01-05', 'South', 'Bengaluru', 'Electronics', 'Wireless Mouse', 2, 799, 1598),
(2, '2026-01-08', 'South', 'Mysuru', 'Grocery', 'Rice 5kg', 3, 420, 1260),
(3, '2026-01-12', 'West', 'Mumbai', 'Fashion', 'Cotton Shirt', 2, 899, 1798),
(4, '2026-01-18', 'North', 'Delhi', 'Electronics', 'Headphones', 1, 2499, 2499),
(5, '2026-01-22', 'East', 'Kolkata', 'Grocery', 'Tea Pack', 5, 180, 900),
(6, '2026-02-03', 'South', 'Bengaluru', 'Fashion', 'Running Shoes', 1, 3299, 3299),
(7, '2026-02-07', 'West', 'Pune', 'Electronics', 'Keyboard', 2, 1499, 2998),
(8, '2026-02-11', 'North', 'Jaipur', 'Grocery', 'Cooking Oil', 4, 160, 640),
(9, '2026-02-16', 'East', 'Kolkata', 'Fashion', 'Denim Jeans', 2, 1599, 3198),
(10, '2026-02-21', 'South', 'Hubballi', 'Electronics', 'Power Bank', 2, 1199, 2398),
(11, '2026-03-02', 'West', 'Mumbai', 'Grocery', 'Dry Fruits', 2, 650, 1300),
(12, '2026-03-06', 'North', 'Delhi', 'Fashion', 'Winter Jacket', 1, 2899, 2899),
(13, '2026-03-10', 'South', 'Mysuru', 'Electronics', 'Smart Watch', 1, 3999, 3999),
(14, '2026-03-15', 'East', 'Kolkata', 'Grocery', 'Coffee Pack', 4, 250, 1000),
(15, '2026-03-20', 'West', 'Pune', 'Fashion', 'Backpack', 2, 1299, 2598),
(16, '2026-03-25', 'South', 'Bengaluru', 'Grocery', 'Almonds 500g', 3, 450, 1350),
(17, '2026-04-02', 'North', 'Jaipur', 'Electronics', 'Bluetooth Speaker', 1, 2199, 2199),
(18, '2026-04-07', 'West', 'Mumbai', 'Fashion', 'Formal Trousers', 2, 1399, 2798),
(19, '2026-04-13', 'South', 'Hubballi', 'Grocery', 'Masala Pack', 6, 120, 720),
(20, '2026-04-19', 'East', 'Kolkata', 'Electronics', 'USB Drive', 3, 699, 2097),
(21, '2026-04-23', 'South', 'Bengaluru', 'Electronics', 'Monitor', 1, 8999, 8999),
(22, '2026-05-04', 'West', 'Pune', 'Grocery', 'Olive Oil', 2, 550, 1100),
(23, '2026-05-09', 'North', 'Delhi', 'Electronics', 'Webcam', 2, 1799, 3598),
(24, '2026-05-14', 'South', 'Mysuru', 'Fashion', 'Kurta', 3, 999, 2997);
select * from sales;
select sum(total_amount) as total_revenue from sales; 
select avg(total_amount) as avarage_sales from sales;
select max(total_amount) as highest_sales from sales;
select min(total_amount) as lowest_sales from sales;

select region, sum(total_amount) AS total_sales from sales group by region;

select category, sum(total_amount) as category_revenue, count(*) AS total_orders from sales group by category;

select date_format(sale_date, '%Y-%m') as sales_month,
    sum(total_amount) as monthly_revenue
from sales
group by date_format(sale_date, '%Y-%m')
having sum(total_amount) > 50000;

select sale_id,region,sale_date,total_amount, sum(total_amount) over (PARTITION BY region ORDER BY sale_date, sale_id
    ) as running_total FROM sales;

select
    sale_id,
    sale_date,
    region,
    city,
    total_amount,
SUM(total_amount) over (
        PARTITION BY region
        order by sale_date, sale_id
    ) AS running_total
from sales
order by region, sale_date, sale_id;




