---
title: SQL-Study-Note-5 - Stored Procedure and User Defined Functions
date: 2022-04-16 19:01:32
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL stored procedures and user-defined functions for encapsulating reusable query logic."
---

{% asset_img sql.jpg SQL Study Note 5 cover: Stored Procedures and User-Defined Functions %}

# Stored Procedure

## Motivation

Generally, developers prefer not to interpret string as SQL codes / instructions due to security concerns. <!-- more --> You can *wrap* the query and update functionality with Stored Procedure. DBMS is able to further optimize the stored procedure and enhance the security. The stored procedure itself is similar to a function implementation.

## Syntax Implementation
``` SQL
DELIMITER $$
CREATE PROCEDURE get_clients()
BEGIN
	SELECT * FROM clients;
END $$
DELIMITER ;
```

The reason of changing DELIMITER is that, we need to use **;** to seperate SQL statements within the stored procedure. (**We are forced to do so!**)
This will damage the integrity of our *BEGIN-END* statement block. Thus, we should temporarily change the DELIMITER (into **\$\$**) and change back to **;** after the definition of our stored procedure.

In order to avoid conflict of naming, MySQL would add a pair of ` to the names of databases, tables and columns.
``` SQL
Student -> `Student`  -- Auto-Renamed to avoid conflicts.
```

You can use 
``` SQL
CALL procedure_name()
```
to call the defined stored procedure.

If you are using the workbench of MySQL, you can simply right click **Store Procedures** to create one. In this case you do not need to worry about the delimiter and MySQL would help you with the transformation (Some sort of Syntactic sugar).

## Delete Stored Procedure
``` SQL
DROP PROCEDURE (IF EXISTS) get_clients;
```

## Parameter Setting of Stored Procedure
``` SQL
CREATE PROCEDURE get_clinets ( state CHAR(2) );
-- You must specify the size and type of the passed parameter.
```
After setting the parameter declaration, the parameters can be then used in the procedure for program logic building.
All the parameters are **REQUIRED**. However, they can have **default values**.
***Even if you want to use the default value, you should pass a NULL to the procedure as a placeholder.***
``` SQL
IF state IS NULL THEN SET state = ‘CA’; 
END IF;
-- By using such statement, you can realize default value de facto.
table.col_name  =  IFNULL(para, table.col_name);
-- This one is more concise and thus recommended.
-- If para is NULL, then use the default value.
```

## Parameter Verification and Constraints
``` SQL
IF payment_amount <= 0 THEN
		SIGNAL SQLSTATE '22003'  
		SET MESSAGE_TEXT = ‘Invalid payment amount’;
END IF
-- payment_amount is required to > 0. If not satisfied, a error code of '22003' is raised and the prompting MESSAGE_TEXT is written. 
```
SIGNAL is similar to **throw exception** in other languages. SQLSTATE is the predetermined error code (corresponding to 'out of range' here, refer the documentation).

## Provide Return Value for Stored Procedure
``` SQL
CREATE PROCEDURE `name` (client_id INT, OUT invoices_count INT)
BEGIN
	SELECT COUNT(*) INTO invoices_count FROM invoices;
END
```
This is a syntactic sugar anyway. What MySQL actually does is define two parameters and pass them to the PROCEDURE for updating. Then SELECT the updated parameter.
At the same time, MySQL uses a '@' prefix to identify variables. For an example, 
``` SQL
SET @a = 0;
```

## User Variable and Local Variable
**SET** is used to assign the *User Variable* while **DECLARE** is used to assign the *Local Variable* used within a stored procedure.
``` SQL
DECLARE risk_factor DECIMAL(9, 2) DEFAULT 0;
```

You can assign the declared variable with the following code:
``` SQL
SELECT COUNT(*) INTO risk_factor FROM table;
```

# User-Defined Functions

The only difference between the procedure and function is that function can only return one single value.
``` SQL
CREATE FUNCTION get_risk_f ( client_id INT) -- Must specify the type for the input parameter
RETURNS INTEGER -- The return parameter must have a type too. Function always returns a single value rather than a query result.
DETERMINISTIC -- Optional attribute. Always return the same result for the same id.
READS SQL DATA  -- Optional. This function can read SQL
MODIFIES SQL DATA -- Optional. This function can modify table.
BEGIN
...
RETURN 1;
```
Functions can be deleted with **DROP** keyword as well.
***

