---
title: SQL-Study-Note-15 Optimization Discussion 2 - Optimize the SELECT and Data Manipulation
date: 2022-05-14 11:14:50
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "Other issues which deserve attention when writing SELECT clause."
key_concepts:
  - Query Optimization
series: SQL
series_index: 15
takeaways:
  - Avoid SELECT * in production queries; specify only needed columns to reduce data transfer
  - Use batch INSERT operations instead of single-row inserts for bulk data loading
  - HAVING filters after aggregation and is slower than WHERE which filters before
  - ORDER BY RAND() forces a full table scan; use application-level randomization instead
---

Other issues which deserve attention when writing SELECT clause.

{% asset_img sql.jpg SQL Study Note 15 cover: Optimizing SELECT and Data Manipulation %}
<!-- more -->
# Optimize the SELECT
## Avoid SELECT *
It is not a good habit of writing SQL, since it would disable the optimizer from conducting optimization like **scanning of overlay index**, influencing the selection of **execution plan**, increasing the overhead of **bandwith, IO, memory and CPU**.
- It is suggested to specify the required columan names only.
## Avoid the use of functions with undefined result
In business scenarios such as master-slave replication, the slave would only duplicate the statements executed by the master.
Thus, applying functions  such as `now(), Rand(), sysdate(), current_user()` would generate different result on the master and slave.

- In addition, for functions with uncertain outputs, the generated SQL statements cannot utilize the **query cache**.

## Place small table ahead of big table
When conducting relationship query, MySQL would scan the tables after the FROM keyword from **left to right** (For Oracle, it is right to left).
Thus, there would be a **full table scan** for the first table, so it would be faster and more efficient if the first table has **fewer** records.

## Use alias of table
When connecting multiple tables in SQL, you should assign alia for each table and add the table alia prefix to the column names. Then the **time of parsing** together with the syntax error raised by **ambiguity** can be reduced.

## Use WHERE instead of HAVING
You should avoid using HAVING, as it only filters the result **after** all the records are selected. However, WHERE would filter records before aggregating to reduce the number of kept records and overhead.
HAVING should be used for the filtering of **aggregate results only**.
## Modify the connection order of WHERE clause
MySQL would parse the WHERE clause from left to right, up to down. Thus, we should place the condition which can **filter out the most data** to the very beginning.

## Do not use ORDER BY RAND()
In this case, a random number would be generate for each row and then conduct sorting using the random number as key.
*E.g.*, `select * from student order by rand() limit 5`.
Thus, it results in super low efficiency.

It is recommended to generate primary key at random, and filter by primary key. 

# Optimization of Data Manipulation Language statements
## Insert data in batch
In case of large scale data insertion, INSERT clause with multiple values is recommended as it is faster:
```SQL
insert into T values(1,2); 
insert into T values(1,3); 
insert into T values(1,4);
-- Insert one value at a time, slower

Insert into T values(1,2),(1,3),(1,4);
-- Insert multiple values
```
Reasons of applying the latter one:
1. Reduce the parsing operation of SQL
2. Reduce the number of connecting to the DB
3. Shorter SQL clause can reduce the Network IO cost.
## Proper use of COMMIT 
COMMIT is able to release some resources (after the transaction is finished) to save the cost:
1. The **undo data block** of transaction
2. The data block recorded in **redo log**
3. Release the lock of transaction to alleviate the **contention of lock**. 
## Avoid query the updated data repeatively
MySQL does not support PostgreSQL's syntax of `UPDATE RETURNING`.
This can be realized with variable.

An example of query the updated data:
```SQL
Update t1 set time=now() where col1=1; 
Select time from t1 where id =1;
```
Optimized using variable:
```SQL
Update t1 set time=now () where col1=1 and @now: = now (); 
Select @now;
```
Both the two methods require 2 Network IO. However, the latter avoids visiting the table again, which is much more efficient.

## Setting the priority of query / update
MySQL allows to change the **priority** of different statements for better collaboration of multiple clients (reduce the waiting casued by lock).
We should first find out the type of the application, *i.e.*, **query based** or **update based** so that we can sacrifice one's efficiency to speed up the other's. 

The **default scheduling strategy** is :
1. Write has higher priority over read.
2. At a moment, the write operation for a certain table can happen only **ONCE**. The write requests are handled in the arriving order.
3. Multiple read operations can happen at the same time. MySQL allows you to edit its scheduling via:
	**LOW_PRIORITY**: used for DELETE / INSERT / LOAD DATA / REPLACE / UPDATE
	**HIGH_PRIORITY**: used for SELECT / INSERT
	**DELAYED**: used for INSERT and REPLACE

- It should be noted that if write becomes a LOW_PRIORITY request, then it may be blocked forever if read requests continue to come. The modification can also be only **temporarily** (appended to the end of SQL).

***














