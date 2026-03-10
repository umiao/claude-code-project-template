---
title: SQL-Study-Note-12 Common Table Expression and Discussion on UNION
date: 2022-05-04 12:17:03
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "Common Table Expression (CTE) is viewed as a better way to realize the functionality of subquery."
---

**Common Table Expression (CTE)** is viewed as a better way to realize the functionality of subquery.

{% asset_img sql.jpg SQL Note of blur! %}

<!-- more -->
- Supported by MySQL >= 8.0
- Generate a named temporary table, only survives during the query
- Comparing with **subquery**: CTE can be referred multiple times within one query, and is able to refer itself (in recursive manner)

# Syntax (of Common Table Expression)
```SQL
WITH cte(col1, col2) AS -- Name the temporary table here, col_name is brackets
(
SELECT 1, 2 UNION ALL SELECT 3, 4
)
SELECT col1, col2 FROM cte
UNION ALL
SELECT * FROM cte -- Can be referred for multipletimes, subquery can be used only once
ORDER BY col1 
```
## Recursively generate sequence
```SQL
WITH RECURSIVE test as -- USE recursive keyword to call itself
(
SELECT 1 AS UNION
UNION ALL
SELECT 1 + n FROM test -- call itself
WHERE n < 10           -- break when n > 10
)
SELECT * FROM test
```
The script above would generate results like:
```SQL
n
1
2
...
10
```
- Another example about querying the quest / reply pairs recursively

``` SQL
WITH RECURSIVE replay ( quest_id, quest_title, user_id, replyid, path ) AS (
	SELECT   -- Select all the answers without reply
	quest_id,
	quest_title,
	user_id,
	replyid,
	cast( quest_id AS CHAR ( 200 ) ) AS path 
	FROM
		imc_question 
	WHERE
		course_id = 59 
		AND replyid = 0    -- 0 means that there does not exist reply
  UNION ALL-- search the reply / comments recursively
	SELECT
		a.quest_id,
		a.quest_title,
		a.user_id,
		a.replyid,
		CONCAT( b.path, ' >> ', a.quest_id ) AS path  
	FROM
		imc_question a -- table a stores the reply of table b
		JOIN replay b ON a.replyid = b.quest_id  
		-- recursively join on table 'reply', that is this very CTE
	) 
SELECT * FROM replay
```

# UNION V.S. UNION ALL
As discussed previously, *MYSQL UNION* is able to combine the results of multiple queries:
```SQL
SELECT column, ... FROM table 1
UNION \ [ALL\]
SELECT column, ... FROM table 2
```
In these SELECT clauses, the corresponding columns should have the same **attributes (column names)**, and the attribute name in the **FIRST** appearing clause would be used as the result's attribute name.

## The main difference of UNION / UNION ALL
When using UNION, MySQL would remove the **duplicates** in the query result. When using UNION ALL, MySQL would return **all the results**, with a **higher efficiency** comparing with UNION.

## Using ORDER BY in UNION sub clause
If **ORDER BY** is used in the sub clause (of SELECT), the result of the sub clauses would first be sorted, before combined.
Besides, the entire sub clause should be wrapped with **brackets**, including **LIMIT**:
```SQL
(SELECT aid,title FROM article ORDER BY aid DESC LIMIT 10) 
UNION ALL
(SELECT bid,title FROM blog ORDER BY bid DESC LIMIT 10)
```
## Using ORDER BY in entire query with UNION
If you want to use **ORDER BY / LIMIT** to restrict or classify the **combined result** of **UNION**, you should add brackets to **each** single SELECT clause:
```SQL
(SELECT aid,title FROM article) 
UNION ALL
(SELECT bid,title FROM blog)
ORDER BY aid DESC
```
## When alia is used
If **alia** is used, then **ORDER BY** clause **MUST** refer the alia:
```SQL
(SELECT a AS b FROM table) UNION (SELECT ...) ORDER BY b
```



