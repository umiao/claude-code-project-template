---
title: SQL-Study-Note-4 - View
date: 2022-04-16 18:39:43
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL Views for storing and reusing query results as virtual tables."
---

{% asset_img sql.jpg SQL Study Note 4 cover: SQL Views as virtual tables %}

# View

## Introduction to View

With the introduction of View, middle / query results can be stored for further query and use, just like a real table.
<!-- more -->

## Creation and Manipulation on View
1. **Creation of View**:
	``` SQL
	CREATE VIEW view_name AS (SELECT …)
	```
	Created Views **would NOT** be stored with the tables. It would be stored in 'Views' instead.

<br>

2. **Alter / Drop of View**:
	``` SQL
	DROP VIEW sales_by_client;
	-- Drop / delete Operation.
	CREATE / REPLACE VIEW AS ...;
	-- REPLACE has the advantage against CREATE that it does not require the view to be dropped in advance.
	```
	Created Views **would NOT** be stored with the tables. It would be stored in 'Views' instead.

	In fact, the Views should be viewed as ***stored query code***. When you need to use them, you can simply rerun the script to retrieve the result. So you can use *version control tools* to store and share them.

<br>

3. **Updatable Views**:
	- Updatable Views stand for those Views who **DO NOT** contain the keywords of **DISTINCT / aggregate functions / GROUP BY / HAVING / UNION**.
	In this case, these Views can be updated via **CREATE / REPLACE**.

	- **Update Opertion**: 
	``` SQL
	UPDATE view_name SET due_date = DATE_ADD(due_date, INTERVAL 2 DAY) WHERE invoice_id = 1l
	```
	Point of updatable views: If you **DO NOT** have the authorization to modify a table, you can still create a View based on that table and update the View, as long as it is **Updatable**.

<br>

4. **WITH CHECK OPTION**:
	If the UPDATE operation may cause some rows to be deleted, you can add **WITH CHECK OPTION** to the end of the **UPDATE** code to prevent this from happening.

***
