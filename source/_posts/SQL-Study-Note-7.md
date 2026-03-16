---
title: SQL-Study-Note-7 - Transactions
date: 2022-04-16 22:07:50
categories:
- [Data Science, SQL]
- [Job Search, SQL]
tags: 
- SQL 
- Data Science
description: "SQL transactions and ACID principles for ensuring data integrity."
key_concepts:
  - SQL Transactions
series: SQL
series_index: 7
takeaways:
  - ACID properties (Atomicity, Consistency, Isolation, Durability) guarantee reliable transactions
  - Higher isolation levels provide more consistency but reduce concurrency and performance
  - Use ROLLBACK to undo all changes in a transaction when any step fails
  - Read Uncommitted is fastest but risks dirty reads; Serializable is safest but slowest
---

<!-- {% asset_img sql.jpg SQL Study Note 7 cover: Transactions and ACID Principles %} -->

# Transactions


1. **Principles of Transaction (ACID)**
	- Atomicity
	- Consistency
	- Isolation
	- Durability
<!-- more -->
``` SQL
START TRANSACTION;
// Instruction block to be executed

-- If only part of the transaction is done and the connection to server is lost, the finished part would be rolled back
COMMIT;
```
A transaction would **lock** the lines and tables to be updated so that they are **untouchable** to other transactions. 
If one transaction comes into locked resources, it would **wait** the owner of the lock to finish, or until it expires the time limit itself.
At the same time, **ROLLBACK** is also a SQL instruction and keyword.


2. **Different level of transaction isolation**:
	{% asset_img iso.jpg Levels of Isolation %}
``` SQL
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
-- Note that this setting is session-leveled.
```

	It comes with the tradeoff that the higher the isolation level is, the lower performance it reaches. (In extreme situation, serializable level would not benefit from distributed architecture.) 

	- **Read Uncommitted**: May read uncommited data (dirty read). Rarely used in actual application as the performance improvement is very limited.
	- **Read Committed**: Default level for most DBMS (Oracle, SQL server). However, it may counter **Nonrepeatable Read**: same select may have different result within one transaction. 
	This is due to the **UPDATE** operation made by other transactions and can be solved by **Line Level Lock**.
	- **Repeatable Read**: Applied with **Line Level Lock**. However, it can still encounter **Phantom Reads** (caused by the delete / insert operations made by other transactions). Require **Table Level Lock** to solve.
	- **Serializable**: Ban the parallel processing and sort all the transactions.

***