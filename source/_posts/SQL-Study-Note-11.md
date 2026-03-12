---
title: SQL-Study-Note-11 User and Privilege Management
date: 2022-04-21 12:39:39
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "Most data science practitioners would not be granted the privilege of managing the database system (not even the privilege to update / delete), so..."
---
{% asset_img sql.jpg SQL Study Note 11 cover: User and Privilege Management %}

>Most data science practitioners would not be granted the privilege of managing the database system (not even the privilege to update / delete), so...
<!-- more -->
## Create and Manage User
``` SQL
CREATE USER join@'%.google.com' IDENTIFIED BY '1234';
-- You can restrict the domain of user with this method.
-- You can also specify an ip after '@'.
-- '1234' Stands for the password.
SELECT * FROM mysql.USER;
-- Retrieve the information of all the users.
-- It is also supported to use GUI interface to manage the user,\
-- their host to log in with, etc
DROP USER bob@gmail.com;
-- Drop a user.
SET PASSWORD (john) = '1234';
-- Reset a user's password.
-- It is also supported to EXPIRE PASSWORD for one user.
-- So that he would be required to change the password by next log in.
```

## Privilege Management
``` SQL
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE 
ON sql_store.* 
TO user_a;
-- An example of granting the privileges.
SHOW GRANTS;
-- Show all the grants
REVOKE privilege .. ;
-- Revoke specified granted privilege.
```
Refer documentation for more related instructions.
***
