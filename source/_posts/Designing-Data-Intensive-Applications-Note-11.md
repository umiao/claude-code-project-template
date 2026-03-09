---
title: Designing Data-Intensive-Applications-Note-11
date: 2024-02-26 20:01:56
categories:
- [Data Science, Data System]
tags:
- DataScience
- Data System
- Designing Data-Intensive-Applications
---
Discussion on implementation and optimization of replication log.
{% asset_img cover.png ML_note %}
<!-- more -->


### Statement-based Replication
- Simplest case, just forward all leader's write request to its followers (`INSERT`, `UPDATE`, `DELETE`).
- Statement calls a **non-determinsitic** function like `RAND()` can get a different value.
- For **auto-incrementing** column / operators relying on the **existing** data in the database, they have to be executed in exactly **the same order** on each replica. This can be limiting in multiple concurrently executing transactions case.
- Stataments that have side effects (**triggers**, **stored procedures**, **user-defined functions**) may result in different side effect occuring on each replica, unless they are absolutely **determinsitic**.

These issues can be resolved by replacing non-deterministic function calls with a fixed value. However, there are too many **edge cases** so other replication methods are preferred.

**Statement-based** replication was used in **MySQL** before version 5.1. It is still sometimes used today, as it is quite compact, but by default MySQL now switches to **rowbased replication** if there is any **nondeterminism** in a statement.
**VoltDB** uses statement-based replication, and makes it safe by requiring transactions to be **deterministic**

### Write-ahead log (WAL) shipping
In storage engines, for data on disk, we usually every write is appended to a log:
- In the case of a **log-structured** storage engine,this log is the main place for storage. Log segments are **compacted** and **garbage-collected** in the background.
- In the case of a B-tree, which overwrites individual disk blocks, every modification is first written to a **write-ahead log** so that the index can be restored to a consistent state after a crash.
- In either case, the log is an **append-only** sequence of bytes containing all writes to the database. 
- We can use the exact same log to build a **replica** on another node: besides writing the log to disk, the leader also sends it across the network to its followers to build a copy of the exact same data structures as on the leader (used in **PostgreSQL** and **Oracle**).
- **Disadvantage**: log describes the data on a very low level, contains details of which bytes were changed in which disk blocks. This makes replication closely **coupled** to the storage engine. 
If the database changes its storage format from one version to another, it is typically not possible to run different versions of the database software on the leader and the followers.
- If the replication protocol allows the follower to use a newer software version than the leader, you can perform a **zero-downtime** upgrade of the database software by first upgrading the followers and then performing a failover to make one of the upgraded nodes the new leader. If the replication protocol does not allow this version mismatch, as is often the case with **WAL shipping**, such upgrades require **downtime**.

### Logical (row-based) log replication
An alternative is to use **different** log formats for replication and for the storage engine, which allows the replication log to be **decoupled** from the storage engine internals. 
This kind of replication log is called a **logical log**, to distinguish it from the storage engine’s (**physical**) data representation.

- A logical log for a relational database is usually a **sequence of records** describing writes to database tables at the granularity of a **row**:
- For an **inserted** row, the log contains the new values of all columns.
- For a **deleted** row, the log contains enough information to uniquely identify the row that was deleted. Typically this would be the *primary key*, but if there is no primary key on the table, the old values of all columns need to be logged.
- For an **updated** row, the log contains enough information to uniquely **identify** the updated row, and the new values of all columns (or at least the new values of all columns that changed).

A transaction that modifies several rows generates several such log records, followed by a record indicating that the transaction was committed. 
MySQL’s **binlog** (when configured to use row-based replication) uses this approach.

Since a logical log is **decoupled** from the storage engine internals, it can more easily be kept **backward compatible**, allowing the leader and the follower to run different versions of the database software, or even different storage engines.

A logical log format is also easier for external applications to parse. This aspect is useful if you want to send the contents of a database to an external system, such as a **data warehouse** for offline analysis, or for building **custom indexes** and **caches**. 
This technique is called **change data capture**.


### Trigger-based replication
Above replication approaches are implemented by the database system, without involving any **application code**. 

- More flexibility may be needed. 
- For example, if you want to only replicate a **subset** of the data, or want to replicate from one kind of database to another, or if you need **conflict** resolution logic, 
- You may need to move replication up to the **application layer**.

**Oracle GoldenGate**, can make data changes available to an application by reading the database log. 

An alternative is to use features that are available in many relational databases: **triggers** and **stored procedures**.

1. A trigger lets you register custom application code that is automatically executed when a data change (**write transaction**) occurs in a database system. 
2. Able to log this change into a **separate** table, from which it can be read by an external process. 
3. That external process can then apply **any** necessary application logic and replicate the data change to another system. 
**Databus** for **Oracle** and **Bucardo** for **Postgres** work like this, for example.

#### Trigger-based replication v.s. built-in replication
- Greater overheads
- More prone to bugs and limitations
- More flexibility.



