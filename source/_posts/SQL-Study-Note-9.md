---
title: SQL-Study-Note-9 Data Modeling, Constraint and Normalization Form
date: 2022-04-20 15:22:22
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- DataScience
---

{% asset_img sql.jpg SQL Note of blur! %}

# Data Modelling Pipeline
1. Understand the requirements; 
2. Build a conceptual Model; 
3. Build a logical model; 
4. Build a physical model.
<!-- more -->

# Foreign Key Constraint

Although modify the primary key IS NOT recommended, we would consider the update to the foreign key caused by the primary key anyway.

**Option (strategy of updating):**
1. **restrict**: restrict modification
2. **cascade**: update the foreign keys according to the primary key
3. **set null**: set the corresponding foreign key in the foreign table into NULL
4. **no action**: reject the update 

It is highly not recommended to use ***set null***, as it would result in organ record in the corresponding tables (no idea which id it belongs to).

# Dataset Normalization

## NF-1 (First Normal Form):
Each record unit (element specified by row and column index) should contain a **single value** only and contain **NO** duplicate column. 
*E.g.*, if you want to add tags to the Course table, you should extract tags into an independent table (and use id mapping to retrieve the tags) for it to be extendable.

## NF-2 (Second Normal Form):
Frist is to satisfy **NF-1**. Also, every non candidate-key attribute depends on the whole candidate keys (that is to say, they must not depend on a true subset of the candidate keys).

That is to say, each table should contain exactly one entity category only. *E.g.*, a table stores course information should **NOT** contain information like the enroll time of each student. If there is an attribute which does not belong to the entity represented by this table, **create a new table** to store it.

## NF-3 (Third Normal Form):
Frist is to satisfy **NF-2**. 
Also, all the attributes of the table should be determined by **candidate key** (for example, id) and should **NOT** be determined by the other non-primary attributes.
That is to say, all the columns of the table should **NOT** be generated / derived by the other columns, to avoid errors caused by duplicate storage and erroneous update.


# Data Model $ \leftrightarrow$ Table
In MySQL, you can use **forward engineer** to convert data model into actual tables. Its essence is to generate **sql script** for database / table generation, with the specified data model / structual graph.
The script would be like:
``` SQL
CREATE schema IF NOT EXISTS … 
USE schema … 
CREATE TABLE …
```
It is also supported to regenerate and fix the table via modifying the data model. In this case, you should select **synchronize model** instead of forward engineer.

For those table with **foreign keys**, if you want to update the table, foreign keys would prevent you from doing so (as a constraint). You should first **drop** all the foreign keys and then reconstruct it to link to correlated tables.

## Reverse Engineer
It is also supported to generate data model (graphs) from existing tables. That is reverse engineering.
It is highly recommended that you only put **ONE** database into a single data model, unless these databases are really **highly correlated**.

## Data Management Opertion (Via SQL Script)
Create of Database:
``` SQL
CREATE DATABASE IF NOT EXISTS name;
-- Make well use of EXISTS clause to avoid error.
```
### Create Table:
``` SQL
CREATE TABLE cus (
	c_id, 
	INT PRIMARY KEY AUTO_INCREMENT,  
	first_name VARCHAR(50) NOT NULL, 
	points INT NOT NULL DEFAULT 0, 
	email VARCHAR(250) NOT NULL UNIQUE
	)
```
### Use Alter Table to update Table:
``` SQL
ALTER TABLE customers 
ADD 
last_name VARCHAR(50) NOT NULL 
AFTER 
first_name

-- You can also use MODIFY / DROP instead of ADD to edit and delete the existing and known columns. 
```

### Add Constraints (e.g., Foreign Key):
``` SQL
FOREIGN KEY fk_col_name (c_id 表中列名) 
REFERENCES customers(c_id) 
ON UPDATE NO ACTION 
ON DELETE NO ACTION 
-- You cannot drop a table without droping its foreign key constraints in advance.
```

## Charset
``` SQL
SHOW CHARSET; 
-- You can use this command to show the charset.
CREATE / ALTER DATABASE db_name CHARACTER SET lain1;
-- About modifying / altering the charset (for a dataset).
CREATE / ALTER TABLE () CHARACTER SET latin1;
-- You can set the charset in the table level, too.
-- Also, charset can be set in column level, just like adding constriants like 'NOT NULL'
```

## Database Engine / Storage Engine
``` SQL
SHOW ENGINES; 
-- Show all the engines.
ALTER TABLE customers ENGINE = InnoDB;
-- Specify the engine for a table.
```

***









