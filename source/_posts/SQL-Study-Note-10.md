---
title: SQL-Study-Note-10 Index
date: 2022-04-21 10:53:59
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "Index can be used to find the row (line) numbers corresponding to the value being queried. Index is added to certain columns and is stored in memory (RAM) fo..."
key_concepts:
  - Database Indexes
  - Query Optimization
series: SQL
series_index: 10
takeaways:
  - Indexes accelerate reads but add overhead to writes and storage; index selectively
  - Use EXPLAIN to analyze query execution plans and identify performance bottlenecks
  - Composite index column order matters; queries must use the leftmost prefix to benefit
  - Full-text indexes with MATCH AGAINST enable efficient text search across large datasets
---
<!-- {% asset_img sql.jpg SQL Study Note 10 cover: Database Indexes %} -->

**Index** can be used to find the row (line) numbers corresponding to the value being queried. Index is added to certain columns and is stored in memory (RAM) for most times.
<!-- more -->

# Create Index
Index can **speed up** the query, however, it would also increase the **size (memory comsuption)** of database as well as the **cost of maintenance**. It is usually implemented by **binary tree** in database systems.
``` SQL
CREATE INDEX idx_state ON customers (state);
-- Specify a column of a table to create an index.
```
# Explain and ANALYZE
``` SQL
EXPLAIN SELECT * FROM ...
```
Add *EXPLAIN* before a sql query would get **explanatory information** instead of the query result. E.g., which information is used and how many records are went through, for performance evaluation.
``` SQL
SHOW INDEXES IN customers;
-- Reveal all the indexes in the customers table.
-- You can find out the indexes added, the cardinality and name.
ANALYZE TABLE customers;
-- Indexes includes primary index, secondary index, etc.
-- You can use the ANALYZE command to view the statistics and values of a table
```
# Different Index Types
1. **prefix index**
You should create prefix index, instead of index on the entire column, for acceleration.
``` SQL
CREATE INDEX idx_n ON customers (last_name(20));
-- In this case, the last_name column would be grouped and indexed according to the first 20 characters only.
COUNT (DISTINCT LEFT(last_name, 10));
-- You can use this way to analyze the performance of creating prefix index on the first 10 characters. 
-- If the number of distinct values is large enough, then this prefix is able to differentiate the possible values.
```
2. **Full-Text Index**
The idea of such index is similar to the implementation principles of **Search Engines**. For all the non-stop words, record the corresponding passages (rows) and the position where they appear.
``` SQL
CREATE FULLTEXT INDEX idex_t_body ON posts (title, body);
-- FULLTEXT INDEX can monitor multiple columns.
SELECT * FROM posts WHERE MATCH(title, body) AGAINST ('react redux');
-- Search 'react redux' in the two columns: title and body. They are viewed as TWO words.
MATCH(title, body) AGAINST ('react -redux +form' IN BOOLEAN MODE);
-- It is possible to exclude some words by adding a '-'.
-- So the above query matches contents including react/form and without redux.
```
3. **Composite indexes**
Enable indexing on **multiple** columns in order to solve the issue that too many results are returned after filtering with the primary index. You can use the appearing order of the columns to decide the filtering priority of the Composite indexes.
``` SQL
CREATE INDEX idx_n ON customers (last_name, state, points);
```
>1. MySQL supports Composite index to include at most **16** columns. However, including 4-6 columns is fairly enough in practice.
>2. At the same time, Composite index supports ***sorting*** on the columns so that the more frequently used columns appear ahead.
>3. In fact, you can decide the **priority** of the indexes being used, by changing the appearing order of the conditions of the **WHERE** clause.
>4. You can use the command of:
	``` SQL
	USE INDEX idx_name;
	``` 
	to force MySQL to use certain index, even it is not optimal.
>5. You can **NOT** make full use of the index, if column is included in the sql expression (**e.g.** in WHERE condtion). So extract the required column first before conducting transformation.

# Sorting and Performance
## Sorting should be avoided as possible
It is because it is **costy**. You should utilize **Indexes** for the purpose of sorting, as possible.
``` SQL
SHOW STATUS;
-- Show the variables being used in MySQL server.
last_query_cost;
-- You can measure the cost of last query by this mean.
``` 
It should be noted that, for column **a** and **b**, **ORDER BY** clause can use the Index for sorting if the order is among one of these:
>1. ORDER BY a
>2. ORDER BY b
>3. ORDER BY a, b
>4. ORDER BY a DESC, b DESC
Any other order would introduce **external sorting** operation (which means **Scaning the Entire Table!**).
There is an exception that if WHERE clause can locate to a **Single Column**, then external sorting would not happen.

If you can achieve the result of query **solely rely on** the index, then it is a **Overlay Index**.

## Duplicate index and Redundant Index
1. **Duplicate Indexes**: Repeatly create **the same** index, *e.g.* on columns (a, b, c).
2. **Redundant Indexes**: One index's functionality is **completely covered** by the other. *E.g.*, creating index for column (a) and (a, b) at the same time. (The latter can cover the prior)


***