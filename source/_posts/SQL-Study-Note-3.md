---
title: SQL Study Note - 3 - Function and the Aggregate Function
date: 2022-04-16 18:34:31
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL built-in functions and aggregate functions including COUNT, MAX, MIN, AVG, and SUM."
---

{% asset_img sql.jpg SQL Study Note 3 cover: Functions and Aggregate Functions %}

# Function and the Aggregate Function
<!-- more -->

1. **Aggregate Function**:
	``` SQL
	COUNT(), MAX(), MIN(), AVG(), SUM()
	```
	It should be noted that **COUNT(row_name)** only returns the number of the non-empty records. If you need to find out the total number of rows, you shoud use **COUNT(\*)**. 
	You can use **COUNT (DISTINCT client_id)** to find out the number of unique client_id, too.

<br>

2. **Non-Aggregate Function**:
	``` SQL
	RAND() -- Generate a random number within (0, 1)
	RAND(seed) -- Specify the rand seed
	SQRT() -- Find the square root for each value
	CONCAT(a, b) -- Concat two strings into one
	```
	Non-aggregate function would return a same-lengthed sequence for the input values. These functions are element-wised.

<br>

3. **GROUP BY clause:**
	- Group the rows according to a given column name. Rows with the same value in the very column would be aggregated together.
	- The order of query clause: IMPORTANT: SELECT -> FROM -> WHERE -> ORDER BY
	- Grouping based on multiple attributes:
	``` SQL
	GROUP BY state, city
	```
	In this case, the grouping would based on the tuple: (state, city)

<br>

4. **Having:**
	``` SQL
	SELECT SUM(res) AS aggregated_res FROM t GROUP BY state HAVING aggregated_res > 100;
	```
	You cannot use WHERE clause to filter the result of the aggreate function, because at that time, the query is not yet completed and the aggregate result is not yet calculated.

	It should be noted that HAVING clause supports the filtering on **Composite Condition**, *e.g.* HAVING aggre_res1 > 10 AND aggre_res2 < 10.

	The HAVING clause is execute after the query is finished. So that it can only filter the **selected** columns. The columns not selected cannot be used in the filtering constraint.
	HAVING **does NOT support alias**.

<br>

5. **WITH ROLLUP:**
	``` SQL
	SELECT SUM(res) AS aggregated_res FROM t GROUP BY state HAVING aggregated_res > 100;
	```
	Conduct an extra aggregate operation for all the aggregated results.
	*E.g.*, the SUM / MEAN of the aggregated results.
	This is **only supported by MySQL**.
	If composite grouping is applied, *e.g.*, GROUP BY col_a, col_b, each group identified by a unique (col_a, col_b) would conduct an extra aggregation.

<br>

6. **Nesting Sub-query:**
	``` SQL
	SELECT * FROM (SELECT ...);
	SELECT * FROM table WHERE col_name IN / NOT IN (SELECT ...);
	```
	*I.E.*, select from the result of another select operation.

<br>

7. **ALL VS ANY / SOME**
	``` SQL
	SELECT * FROM invoices WHERE invoice_total > ALL(SELECT invoice_total FROM invoices WHERE client_id = 3);
	-- Require the records to be greater than ANY of the sub-query results in order to be selected
	SELECT * FROM invoices WHERE invoice_total > ANY / SOME(SELECT invoice_total FROM invoices WHERE client_id = 3);
	-- Require the records to be greater than ONE of the sub-query results in order to be selected
	```
	ANY / SOME are completely **equivalent**. If one value of the sub-query satisfies the logical expression, the '> ANY' expression is satisfied.
	For ALL, only if all the values of the sub-query satisfies the logical expression, the '> ALL' expression can be satisfied.
	**'= ANY'** also equals to **'IN'**.

<br>

8. **Correlated sub-query**
	{% asset_img asso.jpg Associated sub-query %}
	- **Code-writing Order**: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY
	- **Executing Order**: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY
	The marked line is crucial, as the logic of correlated subquery would **retrive one value from the main query at a time**, working in an ***iterative manner***, input the value into the sub-query to ge the result and pass the result back to the main query.
	The main query would check the constraint of WHERE clause and return the result;
	- This means that different alias are required even they points to the same table.
	- Sub-query can touch the alias of the main / outer query.

<br>

9. **EXISTS**
	``` SQL
	SELECT * FROM c WHERE EXISTS (SELECT id FROM I WHERE c_id = c.c_id)
	```
	EXISTS keyword has advantage against the 'IN (sub-query)' manner. This is because the 'IN (sub-query)' needs to finish the sub-query first before the sub-query can return any result to the outer query. However, EXISTS can work as a **short-circuiting operator** which stops immediately when the first results is found.

<br>

10. **Write Sub-query in SELECT / FROM clause**
	- Use SELECT to duplicate the result of aggregate function
	``` SQL
	SELECT (SELECT AVG() FROM t) AS average FROM t;
	```
	This query makes sense because, the aggregate function would only return one single value. If you want to conduct row-wise calculation on the aggregate value, you have to duplicate it.
	- You can also SELECT FROM a sub-query like it is a real-table. However, an alias is required.
		**This may make the query too complicated and should be used with care.**

<br>

11. **Numerical Function**
	``` SQL
	ROUND(num, mantissas_n); 
	-- Round the given number, and mantissas_n decimal places are preserved.
	TRUNCATE(num, mantissas_n); 
	-- Truncate the given number with the decimal setting.
	--Simiarly, we have:
	CEILING()
	FLOOR()
	ABS()
	RAND() 
	```
	Other available functions can be found in the MySQL documentation.

<br>

12. **String Function**
	``` SQL
	LENGTH('sky'); 
	-- Return the length of the input string.
	UPPER('sky');
	--transform to upper case
	LOWER('sky');
	--transform to lower case
	LTRIM() / RTRIM() / TRIM();
	-- Remove the left / right / both side of spaces.
	LEFT(string, n);
	-- Return the left n chars;
	RIGHT(string, n);
	-- Return the right n chars;
	SUBSTRING(string, start, n);
	-- Return n chars starts from start.
	LOCATE('n', 'kinter');
	-- Find the smallest index where the pattern ('n') occurs in the searched string ('kinter'). Index starts from 1.
	REPLACE(string, source, target);
	-- Replace all the pattern of source to target, in string.
	CONCAT(a, b);
	-- Concat strings into 1.
	```
	Refer the documentation for more string functions.

<br>

13. **Time Function**
	``` SQL
	NOW();
	-- Return the current time and date.
	CURDATE();
	-- Return the current date.
	CURTIME():
	-- Return the current time.
	YEAR(time) / MONTH() / DAY() / HOUR() / MINUTE() / SECOND() ...
	-- Extract the year... of a time / date. 
	DAYNAME(time);
	-- Return the name of day, like Friday
	MONTHNAME(time);
	-- Return sth like DECEMBER...
	EXTRACT( YEAR FROM NOW() )
	-- Personalize a date / time.. Year can be substitute with other keywords
	``` 
	**E.g.**, extract order of this year: YEAR(date) = YEAR(NOW());

<br>

14. **Fomat Time / Date**
	``` SQL
	DATE_FORMAT(NOW(), '%y');
	-- %y for 2-digit year, and %Y for 4-digit year;
	-- Similar for D/d/M/m, ...
	-- Can be use to format time as well.
	SELECT DATE_ADD( NOW(), INTERVAL 1 DAY );
	-- Return the date of 1 day later. Accept negative value like -1.
	-- Can Use DATE_SUB instead and the behavior is very similar.
	DATEDIFF(d_1, d_2);
	-- Find the diff of two dates. (by days, the input accepts DATE only)
	-- Result can be negative, calculated by d_1 - d_2.
	TIME_TO_SEC(time);
	-- Transform time to second, starts from 12 am.
	``` 

<br>

15. **IFNULL & COALESCE**
	``` SQL
	SELECT order_id IFNULL(shipper_id, 'Not Assigned') AS s;
	-- If a shipper_id is NULL, return 'Not Assigned' instead.
	COALESCE(shipper_id, comments, ..., 'Not assigned');
	``` 
	The COALESCE is the generalization of IFNULL. The principle is, by offering a bunch of column_name / values, return the first one which IS NOT NULL.

<br>

16. **IF / CASE (Conditional Statement)**
	``` SQL
	IF (expression, first, second);
	-- If the expression is TRUE, then return first; else, return second.

	SELECT order_id 
	CASE 
		WHEN YEAR(order_date) = YEAR(NOW()) THEN ‘Active’
		WHEN YEAR(order_date) = YEAR(NOW()) - 1 THEN ‘Last Year’
		ELSE ‘Other cases’
	END AS category
	FROM orders
	-- The case statement is quite similar with IF statement.
	```
	***