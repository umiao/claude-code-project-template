---
title: SQL-Study-Note-6 - Trigger and Events
date: 2022-04-16 21:46:07
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL triggers and scheduled events for automating database operations."
---

{% asset_img sql.jpg SQL Note of blur! %}

# Trigger

Triggers are the code blocks executed automatically before insertion / update / delete take effect.
<!-- more -->
``` SQL
DELIMITER $$
CREATE TRIGGER payments_after_insert 
AFTER/BEFORE 
INSERT/UPDATE/DELETE 
ON payments FOR EACH ROW
BEGIN   -- You can either write SQL codes here or call the existing procedure
...
END $$
DELIMITER ;
```

## Extensive syntax
``` SQL
NEW -- Return the just inserted line.
OLD -- Return the just deleted line.
NEW.amount -- Can use . to specify a column
```
These two (NEW / OLD) are keywords of MySQL.
Triggers can be used to modify data of any table **EXCEPT** the table which is being listened by the trigger. This is because trigger can trigger itself and results in **infinite loop**.

``` SQL
SHOW TRIGGERS -- Show all the created triggers.
ShOW TRIGGERS LIKE 'c%' -- Filter the triggers.
```
Triggers can be also used for auditing purpose, *i.e.*, record the executor, attribute and timestamp when an operation is done.

# EVENT
Events are periodically triggered codes for multiple tasks.
``` SQL
SHOW VARIABLES -- Show all system variables.
SET GLOBAL event_scheduler=ON / OFF -- Switch the event_scheduler
```

**Create Event**:
``` SQL
DELIMITER $$
CREATE EVENT yearly_delete_state_audit_rows ON SCHEDULE
EVERY 1 YEAR 
STARTS ‘2020-01-01’ ENDS ’2029-01-01’
DO BEGIN  -- Note that DO is required here.
...
END $$
DELIMITER ;
```

**Two ways to calculate the diff of time**:
``` SQL
NOW() – INTERVAL 1 YEAR;
DATESUB(NOW(), INTERVAL 1 YEAR);
```

**Activate / Deactivate Events**:
``` SQL
ALTER EVENT e_name DISABLE;
```
***