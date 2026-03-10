---
title: SQL Study Note - 2 - The Update / Delete / Insert Syntax
date: 2022-04-16 18:29:50
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL data manipulation syntax including INSERT, UPDATE, and DELETE operations with table attributes."
---

{% asset_img sql.jpg SQL Note of blur! %}

# The update / delete / insert syntax
<!-- more -->

1. **The column attributes of table**:
	- PK： primary key
	- NN： Not Null
	- UQ：Unique Index
	- B： binary
	- UN： unsigned data type
	- ZF： zero filled
	- AI： Auto incremental
	- G： Generated column

<br>

2. **Data Type in MySQL**:
	- INT (11): integer with a length of 11
	- VARCHAR(50): array of char with a size $\le 50$.
	- CHAR(50): array of char with a size $= 50$.
	- DEFAULT: Use the given default value to fill this column.

<br>

3. **Insert** data to table:
	``` SQL
	INSERT INTO customers VALUES (DEFAULT, ‘John’, ‘Smith’, ‘1990-01-01’,  NULL, ‘address’, ‘city’, ‘CA’, DEFAULT);
	```
	At the same time, MySQL allows to specify the column names to be assigned values.
	``` SQL
	INSERT INTO customers (first_name, …, state, points) VALUES (…);
	```
	In this case, you do not need to assign the values to the order (of columns) defined by the table.
	The number of affected rows would be returned after successful insertion.

<br>

3. **Insert Multi-rows**:
	``` SQL
	INSERT INTO shippers (name) VALUES ('S1'), ('S2'), ('S3');
	```

<br>

4. **LAST_INSERT_ID**:
	Returns the most recently generated Auto Incremental ID. Enable hierarchical data insertion. *I.E.*, find the ID of the latest inserted data, and then use the id to associate / update other tables.
	This syntax feature can eliminate ambiguity, and it is also convenient to correspond a main table record to multiple sub table records.

<br>

5. **Duplicate Table**:
	``` SQL
	CREATE TABLE orders_archived AS SELECT * FROM orders;
	```
	Use the selected partial / entire data of other table to create a duplicate.
	However, column attributes (constraints) like PK, AI would be ignored.

<br>

6. **Batch Insertion with Select**:
	``` SQL
	INSERT INTO orders_archived SELECT * FROM orders WHERE order_date < ’2019-01-01’;
	```
	Column attributes (constraints) like PK, AI would be ignored as well.

<br>

7. **Truncate Table in workbench**:
	Right click a table and select 'truncate table' would remove all the data (records) but would not remove the table itself.

<br>

8. **Update a single row**:
	``` SQL
	UPDATE invoices SET payment_total = 10, payment_date=’2019-03-01’ WHERE invoice_id = 1;
	```
	Filter the results (single line) that meet the conditions and update the filtered results.
	It is also allowed to use default, arithmetic expression, etc. as the new value of the selected row.

	***Note that even if multiple statements are selected for your filter criteria, MySQL workbench runs in the security update mode by default, allowing you to update only one row at a time. However, in other environments, there is no such problem.***

	*You can drag it to the bottom of SQL editor and choose to uncheck the safe updates option. After changing the settings, you need to reconnect for the settings to take effect.*

	**WHERE attribute IN (1,2,3)** can be used to filter multiple records.

<br>

9. **Use SELECT to UPDATE (apply sub-query in UPDATE)**:
	``` SQL
	UPDATE invoices SET payment_total = 10, payment_date=’2019-03-01’ WHERE client_id = ( SELECT client_id FROM clients WHERE name=’Myworks’ );
	```
	In this manner, a single logical judgement is replaced with a sub-query to update multiple values at a time. 

	If multiple values would be returned in your sub-query, the WHERE clause should be changed to **WHERE client_id IN (sub-query)**.
	You should test the sub-query before update the table.
	You **CANNOT** update the same table where you conduct your sub-query ---- If you have to do so, create a duplicate and give it an alias.

<br>

10. **DELETE**:
	``` SQL
	DELETE FROM invoices WHERE (invoice_id=1);
	```
	Obviously, the condition within the parenthesis can be a sub-query, too.

<br>

11. **Rebuild the Database**:
	``` SQL
	DROP DB If EXISTS DB;
	-- Conduct the script of DB building then.
	```

<br>

***