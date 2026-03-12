---
title: Designing Data-Intensive-Applications-Note-15
date: 2024-03-29 13:52:54
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on transaction related topics."
key_concepts:
  - ACID
  - BASE
  - Transaction Isolation
  - Serializability
  - Two-Phase Commit
takeaways:
  - Use snapshot isolation (MVCC) as the default isolation level for most read-heavy workloads
  - Prevent lost updates with atomic compare-and-set operations rather than application-level read-modify-write
  - Apply serializable snapshot isolation (SSI) when you need serializability without the performance cost of 2PL
  - Watch for write skew and phantom reads which are not prevented by snapshot isolation alone
series: DDIA
series_index: 15
---
Discussion on transaction related topics.
{% asset_img cover.png DDIA Chapter 15 cover: Transactions %}
<!-- more -->

A lot of things may go wrong (database software and hardware / application / network / clients racing / dirty data / concurrency), and that is why we need **transactions**: To group reads and writes together into a logical unit(**commit**), succeeds or fails (**abort**, **rollback**) as one.

Transactions are created for simplifying **programming model** for applications accessing a database, to ignore certain error / concurrency issues, as database has **safety guarantees**.

Transactions on **relational** databases are similar.
As **NoSQL** becomes famous, many databases abandoned transactions or describe a much weaker set of guarantees (due to scalability and availability concern).

### Atomicity, Consistency, Isolation, and Durability (ACID)
Systems that do not meet the ACID criteria are sometimes called **BASE**, which stands for **Basically Available**, **Soft state**, and **Eventual consistency** (also very vague concept).

- **Atomicity**:  **atomic** refers to something that cannot be broken down into smaller parts, means no way a thread can see half-finished result of a operation. 
System can either be in state of **before** operation or **after** opertion.
If a transaction was aborted, the application can be sure that it didn’t change anything, so it can safely be **retried**.

- **Consistency**: Certain statements about your data (invariants) that must always be **true**. E.g., credits and debits across all accounts must be balanced. 
Application is responsible for defining transactions correctly to preserve consistency, not up to the database alone.
- **Isolation**: Multiple clients operating on the same record may run into **concurrency** problems / **race conditions**.
Then we need to isolate transactions. 
However, **serializability** is too expensive to be used, so we often use looser isolation level, e.g., **snapshot isolation**. 
- **Durability**: Data written to **non-volatile** storage (single-node) or copied to some number of nodes (multi-node).

There may **NOT** be perfect solution when choosing between replication and write to SSD / disk.

---

**Multi-Object Transaction**
If multiple objects are to be operated in a transation, then we need to determine which read / write belong to the same transaction.

**In relational DB**: on any particular TCP connection / everything between `BEGIN TRANSACTION` and `COMMIT` is considered to be of the same transaction.

**For non-relational DB**, we may not have such guarantees and ended up with partially updated state.

**Examples** about why multi-object transaction is needed:
1. Keep **foreign key** reference up-to-date.
2. When updating **denormalized** information and keep it in sync (rather than normalized document as a whole).
3. In databases with **secondary indexes**, the indexes also need to be updated.

---

**Single-Object Transaction**
Storage engines universally provide atomicity (can be implemented by **log** for crash recovery) and isolation (use **lock** on each object) on the level of single object (like **key-value pair**).

More complex atomic operations like **increment** operation can be used to remove the need for a **read-modify-write** cycle
Similarly popular is a **compare-and-set** operation, which allows a write to happen only if the value has not been concurrently changed by someone else.

Note that single-object transaction is **NOT** transactions in the usual sense (as it did not group multiple operations on multiple objects into one unit of execution).

---

Retrying failed transaction is not perfect solution:
1. Transaction succeeded but **network** failed, then retrying transaction may cause it perform twice (if without additional **application-level deduplication mechanism**).
2. If the error is due to overload, retrying the transaction will make the problem worse, not better. To avoid such feedback cycles, you can limit the number of retries, use **exponential backoff**, and handle overload-related errors differently (if possible).
3. It is only worth retrying after transient errors (for example due to **deadlock**, **isolation violation**, temporary network interruptions, and **failover**); after a permanent error (e.g., **constraint violation**) a retry would be pointless.
4. If the transaction also has **side effects** outside of the database, those side effects may happen even if the transaction is aborted (like sending emails). This can be solved by **two-phase commit**.
5. If the client process fails while retrying, any data it was trying to write to the database is **lost**.

---
# Weak Isolation Levels

As mentioned before, Serializable isolation is too expensive so people would use **weaker level of isolations** to protect against some concurrency issues, but not all.

### Read Committed
The most basic level of transaction isolation is read committed. It makes two guarantees:
1. When reading from the database, you will only see data that has been committed (no **dirty reads**).
2. When writing to the database, you will only overwrite data that has been committed (no **dirty writes**).

If a transaction needs to update several objects, read committed can guarantee that database is not partially updated (keep **consistency**); 
Also database will not see **later rolled back** data (never actually committed to the database.)

Usually later writes will be delayed until the first write's transaction has committed or aborted.
However, it does not prevent the **race condition** between two counter increments.

It is most common to use **row-level locks** to implement read committed. This is fine for requiring read locks to read, but may have performance issues if such lock is required for write purpose, as it can block a lot of read transactions, bad for **operability** and have **knock-on effect**.

An alternative is, for every object that is written, the database remembers **both** the old committed value and the new value set by the transaction that currently holds the write lock. 
While the transaction is ongoing, any other transactions that read the object are simply given the old value. Only when the new value is committed do transactions, switch over to reading the new value.

### Snapshot Isolation and Repeatable Read
Read Committed may not be sufficient. 
**Non-repeatable read** / **read skew**: Before / after a commit, a different value would be seen. E.g., if you transfer from an account to another, then at certain point, the sum of two account balances may not be accurate.

Some situations can **NOT** tolerate this:
- **Back Up**: During maybe hours of backing up, writes will still be made to the database. Thus, you could end up with some parts of the backup containing an older version of the data, and other parts containing a newer version. If you need to restore from such a backup, the inconsistencies (such as disappearing money) become **permanent**.
- **Analytic queries** and **integrity checks**: Sometimes, you may want to run a query that **scans over** large parts of the database or may be part of a periodic **integrity check** that everything is in order (monitoring for data corruption).  These queries are likely to return nonsensical results if they observe parts of the database at different points in time.

**Snapshot isolation**: each transaction reads from a consistent snapshot of the database, and see the data was committed in the database at the start of the transaction (will not see changes happen after that).

**Implementation**: Use write locks to prevent dirty write; 
a transaction makes a write can block other transactions writing to the same object; 
read is not blocked.
There is **NO lock contention** between reader and writer.

**Multi-Version Concurrency Control** (MVCC): potentially keep
several different committed versions of an object, because various in-progress transactions may need to see the state of the database at different points in time. 

If database only need read committed isolation, then only 2 versions is needed (committed version, and overwritten but not yet committed version). However, MVCC is more frequently used.

#### Implementation
- When a transaction is started, it is given a **unique**, **always-increasing** transaction ID (**txid**).  (You cannot see changes made by a larger transaction ID)
- Whenever a transaction writes anything to the database, the data it writes is tagged with the transaction ID of the **writer**. 
- Each row in a table has a `created_by` field, containing the ID of the transaction that inserted this row into the table.
- Each row has a `deleted_by` field, which is initially empty. If a transaction deletes a row, the row isn’t actually deleted from the database, but it is marked for deletion by setting the `deleted_by` field to the ID of the transaction that requested the deletion. 
- At some later time, when it is certain that no transaction can any longer access the deleted data, a **garbage collection** process in the database removes any rows marked for deletion and frees their space.

**Visibility Rules**:
1. List all other transactions are **in progress** (not committed or aborted), ignore their changes. 
2. Ignore the **aborted** transactions.
3. Ignore writes made by transactions with a **later** transaction ID, regardless of whether they are committed.
4. All other writes are visible.

By never updating values in place but instead creating a new version every time a value is changed, the database can provide a **consistent snapshot** while incurring only a small overhead.

---

### Indexes and snapshot isolation
1. Have the index point to **all** versions of an object, require an **index query** to filter out any object versions that are not visible to the current transaction. When garbage collection removes old object versions no longer visible to any transaction, corresponding index entries can be removed.
2. Like **B-Tree**, we can use an append-only / copy-on-write variant which does not overwrite pages of the tree when they are updated, but instead creates a new copy of each modified page. The parent pages up to the root of the tree, are copied and updated to point to the new versions of the child pages.
3. With append-only B-trees, every write transaction creates a **new B-tree root**, and a particular root is a consistent snapshot of the database at the point in time it was created. (no need to filter on transaction IDs because subsequent writes cannot modify an existing tree, but can only create new roots [needs **compaction** and **garbage collection**])

\* For the 1st method, we can try to fit different versions of the same object on the same page. 
\*\* Snapshot Isolation has many names like **serializable** / **repeatable read**.

### Prevent Lost Updates
Updates may lost, if concurrent applications are in a **read-modify-write cycle**, because the write back value may not contain other application's updates (later write clobbers the earlier write).

This can be resolved by **atomic write** operations, implemented by an **exclusive lock** on the object when it is read so no other transaction can read it until the update has been applied. 
Sometimes it is called **cursor stability**.

Or we can force all atomic operations to be executed on a **single thread**.

Object-relational mapping frameworks make it easy to accidentally
write code that performs **unsafe** read-modify-write cycles instead of using atomic operations provided by the database.


---
**Explicitly Lock**: Also, we can require application to **explicitly lock** objects to be updated, and implement more complex validation logic (like checking whether move of piece of chess is legal)

**Automatically detecting lost updates**: We canc allow writes to execute in parallel, and if the transaction manager detects a lost update, abort the transaction and force it to **retry** its read-modify-write cycle. This is good as it does not require application code to use any special database features.

**Compare-and-set**: The atomic **compare-and-set** opeartion to avoid lost updates by allowing an update to happen only if the value has not changed since you last read it. Otherwise, retry the read-modify-write loop.

**Conflict resolution and replication**: Replicated database has multiple copies on different nodes, make prevention of lost of updates more complex. Lock based / compare-and-set will **NOT** apply as we cannot guarantee that there is a single up-to-date copy of the data, due to asynchrounous write nature. We can allow concurrent writes to create conflicting versions of values (**siblings**) and resolve & merge versions after the fact.
Atomic operations works well with replicated context, especially when they are **commutative**. **Last Write Wins** (LWW) can easily lost updates, but it is widely used.

---

### Write Skew and Phantoms

Some constraints (e.g. checking the inventory before purchase) can be violated, if it depends on certain database data under snapshot isolation, then write happens. After the writes are finished, constraints are violated. This is called **Write Skew**.

Write skew can occur if two transactions read **the same** objects, and then update some of those objects (different transactions may update different objects). 
In the special case where different transactions update the same object, you get a **dirty write** or **lost update** anomaly (depending on the timing).

Atomic operations (because multiple objects involved) and automatic detection will not help. We need **true serializable** isolation to prevent Write Skew.
Otherwise, we can explicitly lock the rows that the transaction dependes on. We can use `FOR UPDATE` to lock all the read rows.

---

The effect, where a write in one transaction changes the result of a search query in another transaction, is called a **phantom**
**Snapshot isolation** avoids phantoms in **read-only** queries, but not in **read-write** transactions.

Using `FOR UPDATE` to lock rows will not work, if no row is returned. Then, it cannot resolve conference room booking problem, because we want to create a meeting if there does not lie one.

**Materializing Conflicts**:
We can try to introduce a lock object into the database to resolve the issue of no object we can attach locks on. However, this can be hard and error-prone, and ugly to let concurrency control mechanism leak into the application data model.
A **serializable** isolation level is much preferable in most cases.

---


## Serializability

We have different ways of implementing serializability:

### Actual Serial Execution
Remove concurrency entirely, but this is only recognizied as feasible only until recently.
This is because: RAM became **cheap** enough to keep entire active dataset in memory; OLTP transactions are usually **short** and only make a small number of read and writes.

**Multi-stage** process (e.g., search and book for flight) is hard to be encapsulated as a transaction. However, humans are very slow to respond, and this will result in huge number of concurrent transactions and mostly **idle**.

Most OLTP applications **avoid** waiting for a user within a transaction.
This means, a transaction is committed within the **same** HTTP request—a transaction does not span **multiple** requests. A new HTTP request starts a new transaction.
\* Even though the human has been taken out of the critical path, transactions have continued to be executed in an interactive client / server style, one statement at a time.
In such case, queries, application codes and database run on different machines and resulted in expensive **communication cost**.
It is **impossible** to disallow concurrency, because database will spend most of the time waiting the application to issue the next query for the current transaction. 

Systems with **single-threaded serial** transaction processing don’t allow **interactive multi-statement transactions**. 
Application must submit the **entire** transaction code to the database as a **stored procedure** (must have all needed data by hand in memory, No network / disk IO).

---

Stored Procedure has kind of bad repuatation because they are implemented with **different langauges** (PL/SQL, e.g.), ugly and archaic, lack **ecosystem** of libraris, harder to **debug**, **version control** , **deploy** and **test**, as well as **monitoring**. Badly written stored procedure may impact the performance more. 

**Solution**: Use exisiting general-purpose programming langauges.
With stored procedures and in-memory data, executing all transactions on a **single thread** becomes feasible

**Partition** may be needed for single thread procedure.
However, procedures may need to be performed in **lock-step** across all partitions, if we need to access multiple partitions (to ensure serializability, may impact performance). 

Data with multiple **secondary indexes** may require a lot of **crosspartition coordination**. 

### Summary of Stored Procedure
- Transaction must be **small** and **fast**
- One slow transaction can stall all transaction processing
- Apply if active dataset can fit in **memory**. It can be slow if we need to access disk.
- Write throughput must be low enough, to be handled on **single CPU** / partitioned **without** requiring cross-partition coordination (possible, but highly limited).


**Two-Phase Locking (2PL)**: Several transactions are allowed to concurrently read the same object as long as nobody is **writing** to it. But as soon as anyone wants to write (modify or delete) an object,
**exclusive access** is required (this lock will block **readers** as well)

2PL is used for **serializable isolation** level in **MySQL** (**InnoDB**) and **SQL Server**, and the **repeatable read isolation** level in **DB2**. 

**Implementation**: **Readers** must first acquire lock in **share mode**; **Writers** must first acquire lock in **exclusive mode**.
Transaction must hold the lock until the end of the transaction (commit or abort), and that is the meaning of two-phase.
**First Phase**: When locks are acquired while the transaction is executing;
**Second Phase**: Locks are release when transaction is finished.

**Deadlock** may happen, and needs to be detected and resolved (by aborting one transaction). So as **contention**. Thus, **2PL** databases may experience severe performance issue, and we may prefer weaker lock in that case.

---

**Predicate locks**: in order to  prevent **phantoms**.
Does **NOT** belong to a particular object (e.g., one row in a table), it belongs to all objects that match some search condition (e.g. certain inventory / conference room availability)

If transaction A wants to read objects matching some condition, it must acquire a **shared-mode** predicate lock on the conditions of the query. 
If another transaction B currently has an **exclusive lock** on **any** object matching those conditions, A must wait until B releases its lock before it is allowed to make its query. 
If transaction A wants to insert, update, or delete any object, it must first check whether either the **old** or the **new** value matches any existing predicate lock. 

The key idea here is that a predicate lock applies even to objects that **do not yet exist** in the database, but which might be added in the future (**phantoms**). 
If **two-phase locking** includes **predicate locks**, the database prevents all forms of write skew and other race conditions, and so its isolation becomes **serializable**.

---

### Index-range locks
**Index-range locks** / **nextkey locking**, which is a simplified approximation of **predicate locking**, might be the reason of poor performance (as it place locks on **more** objects than needed).

E.g., it is safe to block all rooms, or block one room's all slots, if you just want to book a meeting in room A between 1-2PM.
Index-range locks might be easier to implement, with existing indexes.

Index-range lock is still a good compromise to implement serializability. 

---

### Serializable Snapshot Isolation (SSI)
Now used in both single-node and distributed databases.

**Two-phase locking** is a so-called **pessimistic** concurrency control mechanism: if things can go wrong (lock is possessed), we should wait till the lock is released, like **mutual exclusion**.

*Serial execution is extremely pessimistic, equals to each transaction having an exclusive lock during execution.*

**serializable snapshot isolation** is an **optimistic** concurrency control technique. 
We hope everything to turn out alright, just check whether isolation was violated before a transaction commits. If so, we have to retry.

If there lies **high contention**, optimistic concurrency control will have **poor** performance. However, if we have enough spare capacity and reasonable contention, it can perform better. Contention can be reduced with **commutative atomic** operations.	

**SSI** is based on **snapshot isolation**, and adds an algorithm for **detecting serialization conflicts** among writes and dtermines which transaction to abort.

---

Under snapshot isolation, the result from original query may not be up-to-date, because data may be modified during transaction execution, and the premise (that this transaction is doable and correct) may no longer be true (means that the transaction needs to be aborted).

We need to detect reads of a **stale MVCC object version** (uncommitted write occurred before the read), and writes that affect prior reads (the write occurs **after the read**).

1. For detecting **stale MVCC object version**: Before commit a transaction, database checks if any previously ignored transaction (changing the same data field) is committed. If so, current transaction is aborted as its premise no longer exists.
2. For detecting **writes that affect prior reads**: Can be implemented using a technique similar to **index-range lock**, but do not block other transactions. 
We can track in index or table level, when a transaction commits, it detects whether other transactions read the affected data (let such transactions know their read is not up-to-date).





