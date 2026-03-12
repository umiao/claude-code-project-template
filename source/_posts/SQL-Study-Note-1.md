---
title: SQL Study Note - 1 - Syntax Basics
date: 2022-04-16 14:05:53
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL syntax basics covering SELECT, WHERE, JOIN, and fundamental database query operations."
key_concepts:
  - SQL Query Basics
  - SQL Joins
series: SQL
series_index: 1
takeaways:
  - Master SELECT with WHERE, DISTINCT, and logical operators as the foundation of all SQL queries
  - Use appropriate JOIN types (INNER, OUTER, SELF) based on whether you need matching or all rows
  - LIKE and REGEXP provide flexible pattern matching for string filtering
  - UNION combines result sets from multiple queries while removing duplicates by default
---

{% asset_img sql.jpg SQL Study Note 1 cover: Syntax Basics %}

# Overview

1. The core of database system is to interact with **DB (DataBase)** with **DBMS (Database Management System)**.
<!-- more -->

<br>

2. The DB can be generally divided into:
	- **Relational DB** 
	- **NoSQL DB** (*e.g.*, KV (key-value) based DB)

<br>

3. Recommended code style of SQL (Structed Query Language):
	- **Capitalize** all **keywords** and **reserved words**, and lowercase all other contents.
	- Each statement should end with **;**.

<br>

# Keywords and Syntax Rules

## The query syntax

1. **SHOW DATABASES**
	``` SQL
	SHOW DATABASES;
	 ```
 	List all the names of exisitng databases (under the current schema).

<br>

2. **USE**
	``` SQL
	USE database_name;
	SELECT * from table;
	SELECT * from database_name.table; 
	-- Must specify the database_name for the DBs which are not in use
	 ```
 	Select one DB as the default one. 

<br>

3. **SELECT**
	``` SQL
	SELECT (column_name) FROM (table_name) WHERE (condition) ORDER BY (col_name).
	 ```
 	Select the desired data from a table.
 	It should be noted that you should use **=** in SQL to determine equivalence. (It **DOES NOT** mean assignment.) 
 	You can conduct calculation on the selected result.

<br>

4. **AS**
	``` SQL
	SELECT (column_name) FROM (table_name) WHERE (condition) ORDER BY (col_name).
	 ```
 	For each col_name, table_name to be queried and the queried results, you can always to set alias (surname) for them with **AS**.

<br>

5. **-- / comment**
	``` SQL
	-- This a comment.
	// This is also acceptable.
	 ```

<br>

6. **DISTINCT**
	``` SQL
	SELECT DISTINCT column_name FROM t
	 ```
 	Add DISTINCT ahead of the queried target (column) to receive all the unique values.

<br>

7. **AND / OR / NOT**
	``` SQL
	SELECT * FROM t WHERE col_a > 10 and col_b = 'CA'
	 ```
 	Logical operator to be used with the WHERE clause.

<br>

8. **IN**
	``` SQL
	SELECT * FROM t WHERE col_a IN ('A', 'B')
	```
 	Determine if the queried value belongs to a set.

<br>

9. **BETWEEN**
	``` SQL
	SELECT * FROM t WHERE point BETWEEN 100 AND 300;
	SELECT * FROM t WHERE point >= 100 AND point <= 300;
	-- These two are equivalent
	```
 	Determine if the queried value within a given interval.
 	Both ends of the interval are closed ([beg, end]).

<br>

10. **LIKE**
	``` SQL
	SELECT * FROM t WHERE name like 'b%'
	-- Able to match 'Bob' and 'bike'
	```
 	Provide functionality similar to Regular Expression. **%** can match arbitrary string, **_** can match arbitrary char. Not sensitive to the case. 

<br>

11. **REGEXP**
	``` SQL
	SELECT * FROM t WHERE name REGEX '^f[a-z]+d'
	```
 	Match a given Regular Expression pattern.

<br>

12. **IS NULL**
	``` SQL
	SELECT * FROM t WHERE name IS NULL;
	SELECT * FROM t WHERE name IS NOT NULL;
	```
 	Query all the records which are (not) null in a given column. 

<br>

13. **ORDER BY**
	``` SQL
	SELECT * FROM t ORDER BY col_name DESC / AESC
	```
 	Decide the sorting order of the returned records.

<br>

14. **LIMIT**
	``` SQL
	SELECT * FROM t LIMIT offset, tot_num
	SELECT * FROM t LIMIT tot_num
	```
 	Restrict the number of the returned records.
 	Skip the first $n=$offset records and then return tot_num lines of records.
 	Return all the records if number of matched records fewer than tot_num.

<br>

15. **INNER JOIN**
	``` SQL
	SELECT * FROM t_a JOIN t_b on t_a.col_1 = t_b.col_2;
	SELECT * FROM t_a JOIN t_b on t_a.col_1 = DB_2.t_b.col_2;
	-- You can conduct crossed-DB join by specifying the name of the DB not in use.
	```
 	Can be simply writtene as **JOIN**. Concat two tables based on the given condition. Conduct Cartesian product implicitly.

<br>

16. **SELF JOIN**
	``` SQL
	SELECT * FROM t_a AS a JOIN t_a AS b on a.col_1 = b.col_2;
	```
 	A table can join with itself, but different alias are required.

<br>

17. **Multi-table JOIN**
	``` SQL
	SELECT * FROM t_a JOIN t_b on a.col_1 = b.col_2 JOIN t_c on b.col_2 = c.col_3;
	```
 	Multiple (n) tables can be joined but this is not recommended when $ n > 3 $ due to performance concern.

<br>

18. **Composite JOIN / Implicit JOIN**
	``` SQL
	SELECT * FROM t_a JOIN t_b on a.col_1 = b.col_2 JOIN t_c on b.col_2 = c.col_3;
	```
 	Sometimes only a tuple of multiple attributes can uniquely identify a row of the table. In this case, these attributes become Composite Primary Key.
 	``` SQL
	SELECT * FROM t_a, t_b;
	```
 	Implicit JOIN is conducted in the above example but this is not recommended, too.

<br>

19. **OUTER JOIN**
	``` SQL
	SELECT * FROM t_a AS a JOIN t_b AS b on a.col_1 = b.col_2 JOIN t_c AS c on b.col_2 = c.col_3;
	```
 	When using INNER JOIN, some records of the left table cannot match with the right table because the condition of the ON clause is not satisfied. However, if we want to return all the records of the left (right) table regardless of the boolean value of the ON clause, we can use LEFT (RIGHT) OUTER JOIN.
 	You should use RIGHT JOIN instead of LEFT JOIN as possible.
 	**SELF OUTER JOIN** is similar, and alias is still required. 

<br>

20. **USING**
	``` SQL
	SELECT * FROM t_a JOIN t_b on t_a.col_1 = t_b.col_1;
	SELECT * FROM t_a JOIN t_b USING (col_1);
	-- These two are equivalent.
	```
 	Can be used to simplify the code, if the column names of the to-be-joined tables are exactly the same. You can Join on a tuple like 'USING (id1, id2, id3)' and these column names should be exactly the same as well (in the two tables).

<br>

21. **NATURAL JOIN**
	``` SQL
	SELECT * FROM t_a NATURAL JOIN t_b;
	```
 	Let the compiler (DBMS) to decide the way of join. Not recommended to use!

<br>

22. **CROSS JOIN**
	``` SQL
	SELECT * FROM t_a CROSS JOIN t_b;
	```
 	Conduct Cartesian Product.

<br>

23. **UNION**
	``` SQL
	SELECT * FROM a UNION SELECT * FROM b;
	```
 	Concatenate multiple queried results together (on the direction of row). The column names should be exactly the same.
 	**IT SHOULD BE NOTED** that ORDER BY can be set only once, so union all the results before setting the ORDER clause.

***