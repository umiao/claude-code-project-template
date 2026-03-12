---
title: Designing Data-Intensive-Applications-Note-12
date: 2024-03-21 16:27:44
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on replication lag problems and multi-leader replication."
---
Discussion on replication lag problems and multi-leader replication.
{% asset_img cover.png DDIA Chapter 12 cover: Replication Lag and Multi-Leader Replication %}
<!-- more -->


### Problems with Replication Lag
1. Only Asynchronus Replication is realistic, otherwise single node / network failure will turn down the entire system.
2. We may see out-dated data because follower falling behind.
3. **Eventual Consistency**: If writes stopped and wait for followers, followers can catch up and be consistent eventually. 
4. In real world, such latency can be seconds or minutes, bringing real problems.


### Reading Your Own Writes
In certain scenarios, users want to view the changes they submitted **immediately** (post / comment). If we just write to leader and read from follower, the recent changes may not be replicated yet, looks as if they are lost.

Then, we need this **read-after-write** consistency / **read-your-writes** consistency to guarantee that user will always see their own updates after reloading the page (**No** promise for other users, their changes may be shown later).

**Potential Implementations**:
1. Read from **leader** if it is something user may have modified. For something like user profile (only user themself can edit), we can always read from leader.
2. Reading from leader too often can negating the benefit of scaling. Thus we can use some criteria to determine if we read from leader, like: **Track time of last update**, then in the following 1 minute, read from leader; **Monitor replication lag** and do not read from followers left too far behind (> 1 min); Record **Timestamp** of user's update to ensure the served replica reflects the updates, otherwise wait or switch replica. Timestamp can be **logical** (e.g., log sequence number indicating order of writes) or **system clock** (needs **clock synchronization**).
3. If your replica distribute across multiple datacenters, then request must be first routed to the one containing the leader.
4.  **Cross-device** read-after-write consistency may be needed (across desktop and mobile platforms.) This makes recording timestamps and routing to correct data centers more difficult, may need single user's devices be routed to the same datacenter.

### Monotonic Reads
This consistency prevents user from reading data from **the past**.
E.g., a comment was added to a page. During the replication to followers, a user made 2 exactly the same reads. One read returned the comment (from a follower with small lag) and the later one returned **nothing** (due to another follower's greater lag).

This can be implemented by always routing to **the same replica** (map by user ID's hash). Rerouting is needed if the replica failed.


### Consistent Prefix Reads
Replication lag anomalies concerns violation of **causality** (e.g., the answer is shown prior to a question being asked). This is a particular problem in **partitioned / sharded** database.
If different partitions operate independently, then there is no **global ordering of writes** (some part may be new and some may be old).

This requires **consistent prefix reads**, if a sequence of writes happens in a certain order, then anyone reading those writes will see them appear in **the same order**.

We want to have writes which are causally related to each other written to **the same partition**.
This may be hard to achieve in some applications.

### Summary
Root cause of replication lag derived issues is, the replication pretends to be synchronous but in fact is **asynchronous**.
Such issue can be mitigated by conduct some reads on the **leader**.
Many distributed (replicated and partitioned) databases have abandoned the **transactions** as it is expensive in terms of performance and availability. 
**Eventual consistency** may be inevitable in scalable system (may be right but over-simplified)

---  

# Multi-Leader Replication

Having only one leader means we may encounter single point failure on leader, then no writes can be done to the database.

A natural solution is to allow **multiple** nodes to accept writes.
E.g., **Tungsten Replicator** for **MySQL**, **BDR** for **PostgreSQL**, and **GoldenGate** for **Oracle**.

Replication still happens in the same way: each node that processes
a write must forward that data change to all the other nodes. 
We call this a **multi-leader** configuration (also known as **master–master** or **active/active** replication).  
In this setup, each leader simultaneously acts as a follower to the other leaders.

If you have a database with replicas in multiple datacenters, then the leader-based setup will require all writes go into the datacenter containing that leader.

- Among data centers, each leader replicates changes to other leaders (in different datacenter). 
- Within a datacenter, it is regular leader-follower replication.
- Interdatacenter latency can be **hidden** from user, means better preceived latency.
- Allow each datacenter to operate **independently**.
- Have better tolerance of **network problems** (more common as inter-datacenter link is usually on public internet)
- **Challenges**: same data modified in different datacenters must have **write conflicts** resolved. **Autoincrementing keys**, **triggers**, and **integrity constraints** can be problematic. Avoid multi-leader setting if possible.

---

**Clients with offline operation**: Situation where you need multi-leader replication, as you still want to have certain app like calendar to accept read (see meetings) and write (add meetings) even **without** network connection. 
For your devices with the calendar app, they need to be synced when next time online. Every device has a local database that acts as a leader (it accepts write requests) and has a multi-leader replication process.
**CouchDB** is designed for this mode of operation.

**Collaborative editing**: **Etherpad** and **Google Docs** allow multiple people to concurrently edit a text document or spreadsheet.
The changes need to be applied to local replica instantly, and applied to other users' replicas asynchronously.
**Lock mechanism** is needed to avoid editing conflicts. Some tradeoff is needed to make collabration faster, like avoid locking and use **conflict resolution** instead.

### Conflict Detection
In multi-leader setting, conflicts cannot be avoided by synchronous conflict detection (wait for writes to be replicated before return success) as it negated the idea of multi-leader.

**Conflict Avoidance**: Try to ensure all writes of certain record go through the same leader, making it **single-leader** from user's view. It is suggested as conflicts handling is more difficult.
The avoidance can fail if certain datacenter is failed, or the user moved to another physical location and closer to a different datacenter.

**Converging toward a consistent state**:
In single-leader database, the last write determines the value of a field. However, this order is not guaranteed in multi-leader setting, ended up with **inconsistent** result.
Data must be eventually the same in all replicas, thus conflicts must be resolved in a **convergent** way.

**Convergent conflict resolution**
1. Give each write a **unique ID** (a timestamp, a long random number, a UUID, or a hash of the key and value) and pick the write with highest ID as winner and **throw away** other writes.
2. If we use timestamp, then it is **Last Write Wins** (LWW), may cause data loss.
3. Instead, we can give each replica a ID and keep higher numbered replica always take precedence over writes from lower numbered replica. This will also cause **data loss**.
4. Somehow merge the conflict values together (like concatenating)
5. Record the conflict in an explicit data structure that preserves all information, and write application code that resolves the conflict at some later time (perhaps by **prompting the user**).

---

The conflicts resolving logic can be customized, as the most appropriate way may depend on the application.
**On read**: If conflict detected in log of replicated changes, then call the conflict handler. This is usually backend faced and **NOT** interative with user.
**On write**: Store all the conflicting writes and return to application for resolving. (how **CouchDB** works)

Conflict resolution usually applies at the level of individual row / document, not transaction.
(we will count multiple writes of single transaction)

---

## Automatic Conflict Resolution
\* Conflict resolution rules can quickly become complicated, and custom code can be **error-prone**. (e.g., if Amazon only records items in the cart but not items got deleted, then deleted items would be recovered.)

- **Conflict-free replicated datatypes** (CRDTs): 
a family of data structures for sets, maps, ordered lists, counters, etc. that can be concurrently edited by multiple users, and which automatically resolve conflicts in sensible ways. Some CRDTs have been implemented in Riak 2.0
- **Mergeable persistent data structures**: track history explicitly, similarly to the Git version control system, and use a **three-way** merge function (whereas CRDTs use two-way merges).
- **Operational transformation**: conflict resolution algorithm behind collaborative editing applications such as **Etherpad** and **Google Docs**. It was designed particularly for concurrent editing of an ordered list of items, such as the list of characters that constitute a text document.

Note that some conflicts can be **harder** to detect, e.g., make sure each person does not appear in two meeting rooms.

---

## Multi-Replication Topologies
A problem to consider if you have more then **two** leaders. 
Some examples: **circular** (n leaders having n-1 directional edges), **star** (each edge leader has directional link with the central / root leader) or **all-to-all** (each leader has link to each other, most **general** one).
**MySQL** by default only supports **circular topology**.

For star and circular (they may prone to **single point of failure**), a write may need to pass through multiple nodes, so we need each node to place a unique identifer on the replication log to prevent **infinite replication loops**.
For all-to-all topologies, some network links may be faster, the change log may not be delivered in order. 
E.g., dependent update arrives before the insert.
Then we need to resolve this problem of **causality**, to have a node process the insert first by having a timestamp.

It should noted that conflict detection techniques are **poorly** implemented in many multi-leader replication systems.




