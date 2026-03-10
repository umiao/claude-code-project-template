---
title: SQL-Study-Note-8 - Data Type of MySQL
date: 2022-04-16 22:47:13
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "MySQL data types including VARCHAR, TEXT, and best practices for type selection."
---

{% asset_img sql.jpg SQL Note of blur! %}

# Data Type of MySQL

1. **Suggestion for Data Type Selection**
<!-- more -->
	- **VARCHAR**: For short string set to 50, for long string set to 255. Maximum length is 65535, 64KB. (Note that Char Type is fix-lengthed).
	- **MEDIUMTEXT**: 16M document / **LONGTEXT**: 4GB document / **TINYTEXT**: 255 Bytes / **TEXT**: equal to VARCHAR, 64KB
	Note that Chinese charcter takes 3 Byte each, so we allocate $3n$ Bytes to string with length of $n$ (pick the upper bound).
	- Integer Type: **TINYINT**: 1 Byte, **UNSIGNED TINYINT** and **SMALLINT** : 2 Byte, **MEDIUMINT**: 3 Bytes, **INT**: 4 Bytes, **BIGINT**: 8 Bytes.
	***Leading zero filling is supported***: INT(4) -> '0003'
	- Float Type: **DECIMAL(p,s)** defines the int length and decimal length, it can be viewed as a fixed-point decimal (int).
		**DECIMAL = DEC = NUMERIC = FIXED**
		**FLOAT**: 4 Bytes, **DOUBLE**: 8 Bytes  (Expressed in exponential form)
	- Boolean: **BOOL** / **BOOLEAN**, 1 bit
	- Enumerate Type: **ENUM('a', 'b', 'c')**: value must be selected from the given set. This is not a good design as it is complex to change the domain of legal values, you may even need to rebuild the entire table. It is not reusable itself. 
	Creating a table to store the mapping relationship is recommended.
	- Time: **Timestamp** can only store date up to 2038 AD as it takes 4 Bytes. To store later time, use **Datastamp**.
	- **BLOB for Binary Large Object**: **TINYBLOB** / **BLOB** / **MEDIUMBLOB** / **LONGBLOB** takes 255 Bytes / 65KB / 16 MB / 4 GB, respectively.
	Store files in the **FileSystem** as possible rather than store them in the database. Otherwise, you may come into problems like high memory usage, slow copying, low performance, indirect and complicated IO, etc.
	- **JSON**: In order to set JSON object, you can use string form like: '{ "k":v}'. 
	You can also create the object with function:.
``` SQL
JSON_OBJECT('weight', 10, 'dimensions', JSON_ARRAY(1, 2, 3));
```
	In order to **extract** the attributes included in JSON, you can use 
``` SQL
JSON_EXTRACT(properties, ‘$.weight’);
-- while the properties stand for the desired column name / key of the JSON object. 
JSON_EXTRACT(properties, ‘$.weight.data.sub.time’);
-- You can use multiple dots to get the nested attributes.
properties -> ‘$.weight’; 
-- Semi-CPP syntax is also supported
properties -> ‘$.weight[idx]’;
-- Can specify a certain element of the JSON list use '[]' 
```

	At the same time, it should be noted that the returned results are still in JSON format.
	``` SQL
	properties -> ‘$.weight’;
	-- would return something like "sony", which leads to problem when comparing with other results
	properties ->> ‘$.weight’;
	-- is able to return sony, without ""
	```
	In terms of updating partial attributes, you can use JSON_SET. Here **SET** stands for the motion of setting.
	``` SQL
	SET properties = JSON_SET / JSON_REMOVE
	(properties, ‘$.weight’, 30, ‘$.age’, 10) WHERE id=1
	-- JSON_REMOVE is used to remove attributes
	```
	The above example can be used to set part of the attributes in JSON object properties.













