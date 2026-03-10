---
title: Designing Data-Intensive-Applications-Note-10
date: 2024-02-25 20:37:34
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on distributed system goal and Replication implementations."
---
Discussion on distributed system goal and Replication implementations.
{% asset_img cover.png ML_note %}
<!-- more -->

Distributed System:
- **Motivations**: 
1. **Scalability**
2. **Fault tolerance** / **High availability**
3. **Latency**.

### Scale to Higher Load 
- **Scale up**: under single OS, integrate more CPUs, RAM and disks, under Shared memory architecture. 
- However, single machine solution’s cost grows faster than **linearly**, restricted to single **geographic** location, has **limited** fault tolerance and subject to **bottlenecks** (like IO and memory)

#### Shared-disk architecture 
- Serval machines with **independent** CPU and RMA, but stored data on array of **disks** is shared between the machines
- Connected via a fast network (used in some data warehouse). 
- However, this method’s scalability is also limited by contention and overhead of **locking**.

#### Scale Out
- A **Shared-Nothing** Architecture, also named **horizontal scaling** is more popular. 
- Each (virtual) machine is called a **node**. 
- Each node uses its CPUs, RAM and disks **independently**. 
- Coordination between nodes is done at **software level** with conventional network. 
- No special hardware is reuiqred, so you can use whatever machines for best **price / performance ratio**. 
- Data can be potentially distributed across multiple geographic regions to reduce **latency** and **survive** the loss of an entire data center, also increase **throughput**. 
- With cloud deployment of virtual machines, small companies can still have a **multi-region** distributed architecture.
\*Such solution requires developer to be most cautious about the constraints and tradeoffs. It also introduces additional **complexity** for applications and limits the **expressiveness** of data model you are using. 

---

### Replication v.s. Partitioning:
- Common ways of distributing data across multiple nodes are replication and partition.
**Replication**: 
Keeping a copy of **the same** data on several different nodes, potentially in different locations, provides **redundancy**.

**Partition**:
Splitting a big database into smaller **subsets** called partitions.  

These two ways can go with each other.

---

### Models of Replication:
#### Leaders and Follower:  
- Each node stores a copy of data is called a **replica**. 
- We want to ensure that (if our data can fit into arbitrary node, a simplifying assumption) every write ends up on **all** the replicas. 
- That is why we need **leader-based** replication (**active-passive** or **master-slave** replication). 

**Implementation of Leader-based Replication**:
1. One replica is designated the **leader** (**master** / **primary**). When clients want to write to the database, they must send their requests to the leader, and leader first write the new data to its **local storage**.
2. Other replica known as **followers** (**slaves** / **secondaries** / **hot standbys**), will receive leader’s change as part of **replication log** / **change stream**, updating their local copies by applying all writes in **the same order**.
3. When a clinet wants to read from the database, it can query either the leader or any of the followers. However, writes are only accepted on the leader 
(followers are **read-only** from leader’s view). 

- **Usage as built-in feature of relational DB**: 
- PostgreSQL (since 9.0)
- MySQL
- Oracle Data Guard
- SQL Sever’s AlwaysOn Availability Groups.  

- **Usage as non-relational DB**: 
- MongoDB
- RethinkDB
- Espresso. 

Also used in distributed message brokers like **Kafka**, **RabbitMQ**’s **highly available queues**. 
Also used by some network file systems and replicated block devices.


### Synchronous v.s. Asynchrounous Replication:
In relational DB, this is usually **configurable**. However, in other systems, it is usually hard-coded.

#### Example of Synchronous: 
- Leader get the request, send write request to one of the follower, waiting for its “OK” before return to the client. 
- The leader will continue to wait for the next follower to finish updates. 

**Advantages**: follower is guaranteed to have an **up-to-date** & **consistent** copy, which is usable even leader fails.
**Disadvantages**: the followers might **fall behind** the leader by a long time due to failure, capacity issue or network issues. All follower writes will be **blocked** in this case.
Due to the above reason, usually only 1 follower is **synchronous** and the rest are **asynchronous**. 
If the synchronous follower becomes unavailable, another asynchronous follower will become synchronous. 
[This guarantees 2 up-to-date copy on at least 2 nodes]  
This is sometimes called **semi-synchronous**.

Usually, leader-based replication is configured to be **completely asynchronous**.
If leader fails and not recoverable, any write not yet replicated will lost. 
[**Not** durable write, even confirmed with client]
The good side is that leader can continue processing writes even all followers are falling behind (especially when we have a lot of them).

---

### \*Chain Replication
- **Chain Replication** is a variant of **synchronous** replication that has been successfully implemented in a few systems such as **Microsoft Azure Storage** (which avoid loss of data)

**Basic components** of CR are: 
A sequence (chain) of nodes with 2 special nodes — **HEAD** (receives requests from clients) and **TAIL** (end of the chain, provides the guarantee for consistency). 

Such chain has at least following **properties**:
- Tolerates failure of up to $n-1$ nodes.
- Write performance is around write performance of **P/B** (**Primary / Backup**) approach.
- Cluster reconfiguration happens much faster, in case HEAD failure happens. 
- For other nodes — around the same time as for **P/B**.
It is very important to note that chain replication requires a strong and reliable **FIFO link** between nodes.

#### Implementation: 
- Clients send write requests to the head and read requests to the tail. 
- When the head receives a request, it calculates the **delta** of the states, applies the change and **propagates** the delta down the chain (to successor). As soon as tail receives the delta, it sends **ACK** back through each node to the head. 
- As you can see, if a read request returns some value X, that means it has been saved on **all** nodes.

In each node, we will save: 
**Pending(i)** — list of received requests by not yet processed by the tail.
**Sent(i)** — list of not yet processed by the tail requests, sent to the node’s i successor.
**History(i, key)** — list of changes for the key. It could be either full history or just last value.

Note that:
$History(j, key) \subseteq History(i, key), \forall j \gt i$ and $Sent(i) \subseteq Pending(i), History(i, key) = History(i + 1, key) \cup Sent(i)$

#### Coping with failures:   
We need a special **master process** will: 
- **Detect** a failed node; 
- Notify **predecessor** and **successor** of the failed node; 
- Notify clients if the failed node is either HEAD or TAIL.
We also assume that our nodes are **fail-stop**, means server stops working in case of its failure, never send an incorrect response. Failure is always **detectable** by the master process.

**Basc Approach**: 
- Only write on HEAD and read from TAIL (the only tail, making it a hotspot which is bad; 
- If tail is in another data center, it can slow down the entire chain). 
- When we need a new node, insert it after tail will be easiest (just **copy** the tail state and ask the previous tail to continue transfer requests).   
We can tell that, if head fails, we have $Pending(head) – Sent(head)$ lost; If TAIL fails, we can recover by Node TAIL-1. If other node fails, we can recover based on it predecessor and succesor. 

--- 

### Chain Replication with Apportioned Queries （CRAQ）:
Read only on TAIL can be a **bottleneck**. We want to improve this by allowing read requests to be processed by **all** nodes **but** the TAIL. 
To preserve consistency, we maintain a **version vector** for write requests and will do requests to the TAIL to get latest committed version in case of ambiguity.

For **read** request, HEAD will return the response to clients.
For **write** request, each node except TAIL can return the value back to the client.

Each non-tail node can maintain multiple versions of the same key, and those versions are **monotonically increasing**. 
Each version can be either **“clean”** or **“dirty”**, in the beginning, all versions are **clean**.

- When a node receives a **write** request, it adds the received version to its local list of versions of that key.
- If the node is the TAIL then it marks the version as **clean**, the version now is committed and the tail sends **ACK** back to the head.
- Otherwise — the node marks the version as **dirty** and passes to the next node (**successor**).
- When a node receives ACK from its successor it marks the version as **clean** and removes **all older versions**.

---

- When a node receives a **read** request:
- If the latest known to the node version is **clean** — return it.
- Otherwise — ask TAIL to get last committed version of the given key, which it sends back to the client. (Such version will always exist on the tail by design).

#### Summary: 
CRAQ’s performance grows linearly with the amount of nodes with **mostly read** requests; 
In case of mostly write requests, the performance will be close to the basic approach. 
It can be deployed in **multiple** data center to be physically closer to client. 

CRAQ provides **strong consistency**.
But the TAIL might commit the latest version, before a node sends the response to client. 
We can use **monotonic read** (subsequent read requests don’t go in the past; that is to say, subsequent read should see all changes happened ahead) on the whole chain.


Other consistency provided: 
**Eventual consistency**: the node doesn’t request the latest committed version from the TAIL. 
This will still provide monotonic reads but only on **one** node. (subsequent read requests must hit **the same** node). 
Besides, this allows CRAQ to tolerate **network partitioning** (into independent subnets)
**Bounded Eventual Consistency**: Allow to return dirty version only under some conditions, like **not older** than N revisions or T minutes.

---

### Fast Array of Wimpy Nodes (FAWN):  
Similar to the idea of **Amazon Dynamo** and consistent hash, we map a physical server into serveral virtual nodes, each has its own unique VID, forming a **ring**. 
We have multiple **ranges** formed by virtual nodes, and each VI takes care of the keys **“behind”** it and within the certain range.

Then, to improve fault tolerance, data is replicated over $R$ next virtual nodes in the **clockwise** direction (for example, if $R=2$ then keys from A1 are replicated to B1 and C1, if the chain only has A1-C1). Thus, we get a **chain replication** (basic approach).
**Read requests** are routed to the TAIL, i.e. read from A1 will be routed to C1.
**Write requests** are routed to the head and are propagated to the TAIL.

---

### Setting Up Follower (without downtime):
- We may need to set up new followers due to **failed nodes** / need to **increase replica**. We want the added followers to be accurate. Since the database is changing all the time, copy data from one node to naother is not sufficient. 
Use lock to make file consistent will against our goal of **availability**.

#### Method:
1. Take a consistent **snapshot** of the leader’s database at some point (ideally **without** a lock in the entire databases). 
This may be supported by database infra, or third party tool like **innobackupex** for **MySQL**.
2. Copy the snapshot to the new follower node.
3. New follower connects to the leader and requests all the data changes after the snapshot 
(snapshot should be associated to an exact position in the leader’s **replication log**) 
[such position named as **log sequence number** in **PostgreSQL**, **binlog coordinates** in **MySQL**].
4. After follower processed the backlog of data changes, it is caught up.

#### Node Outage: 
Each node can possibly go done, should be able to reboot without downtime of sysTEM. It can be done by **Catch-up** recovery. 
Each follower keeps a log of data changes received from the leader, and be able to identify the **last** successful transaction before the fault occurred. The follower can request the data changes after the outage and catch up. 

--- 

### Leader Failure: Failover
- In case of the leader failed, one of the followers needs to be **promoted** to the new leader.
- Clients need to be reconfigured to send writes to the new leader 
- Other followers start to consume data changes from the new leader.
- This is called **"failover"**, can be either manually done or automatically done.

### Automatic Failover Process
1. **Determining the leader failed**. Failure reason could be various (crashes, power outages, network issues, ...) but we can simply use **timeout** to detect. If a node doesn’t respond for some period of time—say, 30 seconds—it is assumed to be **dead**.
2. **Choosing a new leader**. This could be done through an **election process** (where the leader is chosen by a majority of the remaining replicas), or a new leader could be appointed by a previously elected **controller node**. 
The best candidate for leadership is usually the replica with the most up-to-date data changes from the old leader (to minimize any data loss). 
Getting all the nodes to agree on a new leader is a **consensus problem**.
3. **Reconfiguring the system to use the new leader**. Clients now need to send their write requests to the new leader. If the old leader comes back, it might still believe that it is the leader,
not realizing that the other replicas have forced it to step down. The system needs to ensure that the old leader becomes a follower and recognizes the new leader.

#### Things Could Go Wrong

- If **asynchronous replication** is used, the new leader may not have received all the writes from the old leader before it failed. 
- If the former leader rejoins the cluster after a new leader has been chosen, what should happen to those writes? 
- The new leader may have received conflicting writes in the meantime. The most common solution is for the old leader’s unreplicated writes to simply be discarded, which may violate clients’ **durability** expectations.
- \* Discarding writes is especially dangerous if other storage systems outside of the database need to be coordinated with the database contents. For example, in one
incident at **GitHub**, an out-of-date MySQL follower was promoted to leader. The database used an autoincrementing counter to assign primary keys to new rows, but because the new leader’s counter lagged behind the old leader’s, it **reused** some primary keys that were previously assigned by the old leader. These primary keys were also used in a **Redis** store, so the reuse of primary keys resulted in **inconsistency** between **MySQL** and **Redis**, which caused some private data to be disclosed to the wrong users.
- Two nodes coul both believe that they are the leader. This situation is called **split brain**
if both leaders accept writes, and there is no process for resolving conflicts, data is likely to be lost or corrupted. 
As a safety catch, some systems have a mechanism to **shut down** one
node if two leaders are detected. However, if this mechanism is not carefully designed, you can end up with **both** nodes being shut down.


A longer timeout means a longer time to recovery in the case where the leader fails. However, if the timeout is too short, there could be unnecessary failovers. (**load spike**, **network glitch** can trigger failovers, and further impact the performance of system)

Thus, many teams prefer to perform failovers **manually**.





