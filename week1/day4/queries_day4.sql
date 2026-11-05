use day3;
SELECT sale_id, product, region,total_amount from sales
where total_amount > (
    select avg(total_amount)
    from sales )
order by total_amount DESC;

select s1.region,
    s1.city,
    SUM(s1.total_amount) AS city_revenue
from sales s1
group by s1.region, s1.city
having SUM(s1.total_amount) = (
select MAX(city_total)
from (SELECT s2.city, SUM(s2.total_amount) AS city_total
from sales s2 WHERE s2.region = s1.region GROUP BY s2.city) AS regional_cities);

with average_sales as (
select avg(total_amount) as avg_amount from sales )
select sale_id,product, total_amount from sales
where total_amount > (
    SELECT avg_amount
    FROM average_sales
);

WITH city_revenue AS (
    SELECT
        region,
        city,
        SUM(total_amount) AS revenue
    FROM sales
    GROUP BY region, city
),
regional_revenue AS (
    SELECT
        region,
        SUM(revenue) AS total_revenue
    FROM city_revenue
    GROUP BY region
)
SELECT *
FROM regional_revenue
WHERE total_revenue > 10000
ORDER BY total_revenue DESC;

SELECT DISTINCT region
FROM sales s1
WHERE EXISTS (
    SELECT 1
    FROM sales s2
    WHERE s2.region = s1.region
    AND s2.total_amount > 5000
);

