---
title: Designing Data-Intensive-Applications-Note-13
date: 2024-03-24 09:31:49
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on leaderless replication."
key_concepts:
  - Leaderless Replication
  - Eventual Consistency
  - Consistency
  - Replication
takeaways:
  - Set quorum parameters w + r > n to guarantee reading the most recent write in leaderless systems
  - Use read repair for frequently accessed data and anti-entropy for background consistency
  - Apply version vectors to track causality and detect concurrent writes across replicas
  - Prefer last-write-wins only when data loss from concurrent writes is acceptable
series: DDIA
series_index: 13
---
Discussion on leaderless replication.
<!-- {% asset_img cover.png DDIA Chapter 13 cover: Leaderless Replication %} -->
<!-- more -->

Some data storage systems take a different approach, abandoning the concept of a leader and allowing **any** replica to directly accept writes from clients.
Become fashion after Amazon used it for **Dynamo** system.
**vi Riak**, **Cassandra**, and **Voldemort** are open source datastores with leaderless replication models inspired by Dynamo, so this kind of database is also known as **Dynamo-style**.

In some leaderless implementations, the client directly sends its writes to several replicas, while in others, a **coordinator node** does this on behalf of the client. 
Difference with leader database: coordinator does not enforce **ordering** of writes.

There is no **failover** in leaderless configuration, we mark write as successful if received enough ack / OK response.
Where failed node return online, it may have stale data due to lost of writes. Thus, a client can send **multiple** read requests and use latest version.

### Read repair and anti-entropy
We want to gain eventual consistency, and catch-up mechanism for replicas in leaderless setting.

**Read Repair**: When a client makes a read to serval nodes in parallel, it can write new values back to the stale replica (works well for data being frequently read).

**Anti-entropy process**: have a background process to check difference in data between replicas and copies missing values. 
This process does **NOT** copy data in particular order and my have big **latency** (this helps recovering the less read values).

### Quorums for reading and writing
We need to determine how many successful read / writes are needed to make sure the changes take effect on enough replicas (do not care why some nodes failed).
Genearlly, we need changes be confirmed by $w$ nodes out of $n$ replicas, and we read $r$ nodes every time. If $w+r \gt n$, then at least one read value is latest.

If $w \lt n$, if node is unavailable, we can still process writes.
If $r \lt n$, if node is unavailable, we can still process reads.
Usually, reads and writes are sent to all $n$ replicas.

\* Note that we can have more than $n$ nodes, but ensure for any given value it is only stored on $n$ nodes. This allows us to partition and store dataset too big to fit in single node.

Often $r$ and $w$ are chosen to be majority ($\gt \frac{n}{2}$) but it is not necessary, it only matters that the sets of nodes used by the read and write operations overlaps in at least one nodes.

If **quorum condition** is not satified (use smaller $r$ and $w$), you may read stale values but allows better performance and availability.
Even **quorum condition** is satisfied, you may still read stale value if **sloppy quorum** is used ($w$ reads and $r$ writes ended up on different nodes so there is no guarantee for overlap).

If two writes occur concurrently, we cannot tell which one happened first. We can **merge** the concurrent writes. 
If a write and read occur concurrently, writes may be reflected on only some of the replicas and stale values may be read.
If a write succeeded on some replicas ($\lt w$), it is not rolled back on the replicas where it succeeded. Also, a node carrying a new value may fail and restored with an older value.

Better **Not** view quorum condition as a strong guarantee for data consistency.

**Staleness** is **hard** to monitor on leaderless setting, as we cannot easily track the replication lag (no fixed order) for metrics analysis.

---

### Sloppy Quorums and Hinted Handoff
Network problem may prevent clients from connecting with active nodes, so the client can no longer reach a quorum.

**Sloppy quorum**: writes and reads still require $w$ and $r$ successful responses, but thoese may include nodes that are not among the designated n "home" nodes for a value.
Default on for **Riak** and default off for **Cassandra** and **Voldermort**. 

**Hinted handoff**: Once the network interruption is fixed, writes which are temporarily accepted on behalf of another node got sent to the "home" nodes.
Tradeoff is that latest values maybe written to other nodes. 
Only durability is guaranteed that data is stored somewhere in $w$ nodes, but may not be visible by $r$ writes until **hinted handoff** is completed.

---

### Concurrent Writes
**Dynamo-style** databases allow several clients to concurrently write to **the same** key, which means that conflicts will occur even if strict quorums are used. 

To achieve eventually consistency, we need to detect and resolve the conflicts (e.g., cause by multiple clients' concurrent writes).

**Last Write Wins (LWW)**: Keep only the most recent value, discard concurrent writes to achieve eventual convergence.

However, for concurrent writes, the order is undefined. By applying and using the LWW, we achieve the eventual convergence at the cost of **durability**. Non-recurrent write may be possible to be dropped.
In some cases like aching, lost writes are maybe acceptable, otherwise **LWW** is not suitable.

The only safe way of using a database with **LWW** is to ensure that a key is only written **once** and thereafter treated as immutable, thus avoiding any concurrent updates to the same key. 
For example, a recommended way of using **Cassandra** is to use a
**UUID** as the key, thus giving each write operation a unique key

 Whether one operation happens **before** another operation is the key to defining what concurrency means. 
 In fact, we can simply say that two operations are concurrent if neither happens before the other (i.e., neither knows about the other, no **causally relationship**) 

### Handling of Concurrent Writes
1. The server maintains a version number for **every** key, **increments** the version number every time that key is written, and stores the new **version number** along with the **value** written. 
2. When a client reads a key, the server returns all values that have not been overwritten, as well as the **latest** version number. A client must read a key before writing.
3. When a client writes a key, it must include the version number from the prior read, and it must **merge** together all values that it received in the prior read. (The response from a write request can be like a read, returning all current values, which allows us to chain several writes like in the shopping cart example.)
4. When the server receives a write with a particular version number, it can **overwrite** all values with that version number or below (since it knows that they have been merged into the new value), but it must keep all values with a higher version number (because those values are **concurrent** with the incoming write).
5. When a write includes the version number from a prior read, that tells us which previous state the write is based on. If you make a write without including a version number, it is concurrent with all other writes, so it will not overwrite anything—it will just be returned as one of the values on subsequent reads (as an new independent copy)

If you want to do a bit more, you can try to merge the above multiple versions into one. However, note that delted items may appear again as the result.
System must leave a **marker** with an appropriate version number to indicate that the item has been removed when merging siblings. 
Such a deletion marker is known as a **tombstone**.

---

### Version Vectors

When we have multiple replicas accepting writes concurrently, we need to use a version number **per replica** as well as **per key**.

1. Each replica **increments** its own version number when processing a write
2. Also keeps track of the version numbers it has seen from each of the other replicas. 
3. This information indicates which values to **overwrite** and which values to keep as **siblings**.

**Version Vector**: The collection of version numbers from all the replicas. Sometimes called a **Vector Clock**.
The version vector structure ensures that it is safe to read from one replica and subsequently write back to another replica. 
Doing so may result in siblings being created, but no data is lost as long as siblings are merged correctly.

### Dotted Version Vector
In case of conflict, instead of Last Write Wins, we can store all the versions, their values and the **Causal Hisotry** (e.g., version 3 declares it is `from: [v_1, v_2]`, means that it overwrites value of version 1 and 2)

However, the causal history may be too expensive to store.

Data structure of **Dotted Version Vector** (DVV) looks like this:
$((i_1, n), [(i_1, m), (i_2, l), (i_3, k) ...])$
Here, $i_1, ..i_3$ are IDs of nodes, and the number $n, m, l, k$ are version numbers (incremental) of corresponding node.

The first part is the version of certain node (called a **dot**), and the second part (list) is the **version vector**, stores the state before the event which added $(i_1, n)$ happens.

Then we can determine the timing / causality. We can use the version vector to determine which event / version comes after the other.
Otherwise, they are **concurrent**. 

