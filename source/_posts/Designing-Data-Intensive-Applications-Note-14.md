---
title: Designing Data-Intensive-Applications-Note-14
date: 2024-03-24 14:21:49
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on partition related topics."
key_concepts:
  - Partitioning
  - Database Indexes
  - Replication
takeaways:
  - Partition by hash of key to distribute load evenly and avoid hot spots
  - Use compound primary keys to enable efficient range queries within a single partition
  - Choose between document-partitioned (local) and term-partitioned (global) secondary indexes based on read/write patterns
  - Prefer dynamic partitioning over fixed partitioning when data volume is unpredictable
series: DDIA
series_index: 14
---
Discussion on partition related topics.
{% asset_img cover.png DDIA Chapter 14 cover: Partitioning and Sharding %}
<!-- more -->

**Partition**: Known as **Shard** in MongoDB, Elasticsearch, and SolrCloud. Known as a **region** in HBase, a **tablet** in Bigtable, a **vnode** in Cassandra and Riak, and a **vBucket** in Couchbase. 

Partition aims to act as independent small, **non-overlapping** databases for better **scalability**.
Different partitions can be placed on different nodes for load balancing (on processor) and large dataset distribution. Each node should be able to independently querying their own partition, able to **parallelize** complex queries.

Old partition databases: **Teradata**, **Tandem NonStop SQL**; Recently: **Hadoop** and **NoSQL** databases.

Partition is usually combined with replication to have each partition stored on multiple nodes. If leader based replication setting is used, then leader and follower of the same partition should belong to different nodes.

---

- We expect partition to be spreading data and query **evenly**, so that our throughput and data volume being able to handle can grow linearly as we have more nodes (if we ignore the replication).
- **Skewed**: the partitioning is unfair and some partitions have more data. Reduce the effectiveness of partition. A partition with high load is named a **hot spot**.
- We should try to assign records to node randomly, preferrably using **primary key**.

**Partition by Key Range**: 
1. assign a **continuous** range of keys (from some minimum to some maximum) to each partition (like encyclopedia)
2. The range of keys are **NOT** guaranteed to be evenly spaced, need to adapt to the data. Some access pattern may lead to **hot spots**.
3. We can keep the keys sorted in each partition to make scan easier and treat the keys as a **concatenated index**.

**Partition by Hash of Key**: 
1. Due to the risk of **skew** and **hot spots**, we can use hash function to determine partition (assign each partition a range of **hashes**).
2. Good hash function can takes skewed data but still makes it **uniformly** distributed. 
3. Such function not have to be **cryptographically** strong if it is for partition purpose. E.g., **MD5** and **Fowler–Noll–Vo**. 
4. Some hash function (used for hash tables) are not suitable for partitioning, like `Object.hashCode()` in **Java** and `Object#hash` in **Ruby**, where same key may have different hash values across processes.
5. The partition boundaries can be evenly spaced, or they can be chosen **pseudorandomly** (**consistent hashing** / **hash partitioning**, randomly choose partition boundaries to avoid the need for **central control** / **distributed consensus**. That is to say, also map nodes / virtual nodes to a ring, then direct traffic to the next node on the ring).
6. We can **NOT** do efficient range queries by hashing the keys. No primary key based range queries as queries have to be sent to all partitions.
\* We can make a tradeoff by using **compound primary key** but just hash the first part to determine the partition, other columns used as **concatenated index**.
E.g., if you use compound key of `(user_id, updated_timestamp)`, you can effectively query posts of one user, in a certain time range. Each user's data is guranteed to be stored in a single partition.

**Relieving Hot Spots**: 
1. Exactly the same keys would still be directed into the **same** partition, even with the partition on hash of keys (e.g., visits to certain celebrity).
2. This is hard to be compensated by data systems, so should be done on the **application level**. The hotspots can be relieved by appending random numbers to the beginning / end of the key. 
3. This only makes sense when you are adding **salt** for small number of hotspots.

---

**Partition on Secondary Indexes**
1. **Secondary Indexes** usually cannot uniquely identify a record, more like searching occurences of a particular value. It is more **complex** and does not map neatly into partitions.
2. **Document-based partitioning** (also named as **Local Index**): Each partition is **sepearate** and owns its own secondary indexes covering the documents in that partition. E.g., you can add a qualified red car to each partition's seondary index's list of `color:red`. During query time, you should send query to all partitions and combine the result back (**scatter / gather**, may make the secondary index more expensive and prone to **tail latency amplification**). It is widely used and ideally you can construct your schema to have secondary index queries served from a **single** partition.
3. **Term-based partitioning**: In this case, we are having **global** secondary indexes which cover data in all partitions. Such index can be stored in partitions in a **non-overlap** manner. E.g., `color:red` contains **all** indexes of qualified cars across partitions, but only got stored in **single** partition (called **term-partitioned** as the term we are looking for determines the partition of index).
4. **Term / Global secondary index** is more efficient in **read**; **write** is slower and more complex (a write to single document may affect multiple partitions of the index).  Global secondary index also require a **distributed transaction** across all partitions
affected by a write, which is not supported in all databases. It is often **asynchronous** and the index may not be updated in real-time.

---

### Rebalance Partitions
**Rebalancing** (move data and requests from one node to another) may be needed due to increase of **query throughput** (to add more CPUs), increase of **dataset size** or **machine failure**.

After rebalancing, we want:  
1. Load (data storage, read and write requests) should be shared **fairly** between the nodes in the cluster.
2. While rebalancing is happening, the database should continue accepting reads and writes.
3. No more data than necessary should be moved between nodes, to make rebalancing fast and to **minimize** the network and disk I/O load.

**Strategies of rebalancing**:
1. **NOT** recommended: **hash mod N** (N is number of new partitions). This is expensive as it over-moves the data. Instead, better divide hash into **ranges** in partitioning.
2. **Fixed number of partitons**: creating **more** partitions than number of nodes, assign several partitions to each node (maybe unevenly). Then partitions can be easily moved between nodes for node extension / delete purpose. Number of partitions nor assignment of keys will chagne. Also, old partitions can still handle requests when transferring is in progress.

---

### Dynamic Partitioning
A **fixed number** of partitions with **fixed boundaries** may end up with all data in one partition, if you did not configure the boundaries properly.

**Dynamic Partitioning** (used in **HBase** / **RethinkDB**): When a partition **grows** to exceed the configured size (e.g. 10GB), it is split into two partitions approximately half of the original size. If data is delted below same threshold, it can be merged with **adjacent** partition.

It makes the number of partitions adapats to the total data volume to potentially save the overhead.

An initial set of partitions can be configured on an empty database (this is called **pre-splitting**) to prevent the number of partitions to grow from 1, but it requires you to know the **key distribution**.

---

### Partitioning proportionally to nodes
**Dynamic partitioning**: number of partitions is proportional to the size of the dataset
**Fixed num‐ber of partitioning**: the size of each partition is proportional to the size of the dataset.

**Proportional Partitioning**: Make each node having a fixed number of partitions, and the number of partitions proportional to the number of nodes.

When a new node joins the cluster, it **randomly** (hash-based partitioning is required) chooses a fixed number of existing partitions to split, and then takes ownership of one **half** of each of those split partitions while leaving the other half of each partition in place. 

The randomization can produce **unfair** splits, but when averaged over a larger number of partitions (in **Cassandra**, 256 partitions per node by default), the new node ends up taking a fair share of the load from the existing nodes. 

---

\* It may be good to loop human in partitioning to reach a **tradeoff** between automatic / manual partitoning, e.g., data system suggests partition assignment but requires commit from admin.
Fully automated partitionings can be unpredictable and expensive, may cause **overload** of network / nodes and **cascading** failure.


---

### Request Routing

**Request Routing** is an instance of **service discovery**, which is about how we route request to certain node / port.

1. Allow clients to contact **any** node (e.g., via a **round-robin load balancer**). If that node coincidentally owns the partition to which the request applies, it can handle the request directly; otherwise, it forwards the request to the appropriate node, receives the reply, and passes the reply along to the client.
2. Send all requests from clients to a **routing tier** first, which determines the node that should handle each request and forwards it accordingly. This routing tier does **NOT** itself handle any requests; it only acts as a **partition-aware load balancer**.
3. Require that clients be aware of the partitioning and the assignment of partitions to nodes. In this case, a client can connect **directly** to the appropriate node, without any intermediary.

Coordination service like **ZooKeeper** can help in this process (as routing tier), but you can also have any node take & forward requests.

\*  **Massively Parallel Processing (MPP)** relational database can be a lot more complex, as query needs to be broken into executive stages and partitions.