create database day2;
use day2;
CREATE TABLE Employees (
    emp_id INTEGER,
    emp_name TEXT,
    dept_id INTEGER
);
CREATE TABLE Departments (
    dept_id INTEGER,
    dept_name TEXT
);
INSERT INTO Employees VALUES
(1, 'Rahul', 101),
(2, 'Priya', 102),
(3, 'Amit', 103),
(4, 'Sneha', 104);
INSERT INTO Departments VALUES
(101, 'HR'),
(102, 'IT'),
(103, 'Finance'),
(105, 'Marketing');
select
    e.emp_id,
    e.emp_name,
    d.dept_name
from Employees e
inner join Departments d
on e.dept_id = d.dept_id;
select
    e.emp_name,
    d.dept_name
from Employees e
left join Departments d
on e.dept_id = d.dept_id;
select
    e.emp_name,
    d.dept_name
from Employees e
right join  Departments d
ON e.dept_id = d.dept_id;
select
    e.emp_name,
    d.dept_name
from Employees e
LEFT JOIN Departments d
ON e.dept_id = d.dept_id
UNION
select
    e.emp_name,
    d.dept_name
from Employees e
RIGHT JOIN Departments d
ON e.dept_id = d.dept_id;

select
    e1.emp_name as Employee1,
    e2.emp_name as Employee2,
    e1.dept_id
from Employees e1
inner join Employees e2
on e1.dept_id = e2.dept_id
and e1.emp_id < e2.emp_id;
INSERT INTO Employees VALUES
(5, 'Kiran', 101),
(6, 'Arun', 102);
SELECT
    e.emp_id,
    e.emp_name,
    d.dept_name
FROM Employees AS e
LEFT JOIN Departments AS d
ON e.dept_id = d.dept_id;