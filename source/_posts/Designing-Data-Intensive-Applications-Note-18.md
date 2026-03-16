---
title: Designing Data-Intensive-Applications-Note-18
date: 2024-05-05 12:00:33
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on challenges with batch processing jobs."
key_concepts:
  - Batch Processing
  - MapReduce
  - Fault Tolerance
takeaways:
  - Use map-side joins (broadcast or partitioned hash join) when one input is small enough to fit in memory
  - Prefer modern dataflow engines like Spark over MapReduce to avoid unnecessary materialization overhead
  - Design batch jobs to be deterministic so failed tasks can be safely retried without side effects
  - Apply the Unix philosophy of composable single-purpose tools to batch processing pipeline design
series: DDIA
series_index: 18
---
Discussion on challenges with batch processing jobs.
<!-- {% asset_img cover.png DDIA Chapter 18 cover: Batch Processing %} -->
<!-- more -->

### Unix Tools (Pipe)

We can categorize systems into: **Serivices**(online systems), **Batch Processing Systems** (offline systems) and **Stream processing system** (near real-time).

The **Unix** philosophy in data processing: concatenate data input and output to form data flows, using `pipe`.

1. Make each program do **one thing** well. To do a new job, build a fresh rather than complicate old programs by adding new “features”.
2. Expect the output of every program to become the input to another, as yet unknown, program. Don’t clutter output with extraneous information. Avoid stringently columnar or binary input formats. Don’t insist on interactive input.
3. Design and build software, even operating systems, to be tried early, ideally within weeks. Don’t hesitate to throw away the clumsy parts and rebuild them.
4. Use tools in preference to unskilled help to lighten a programming task, even if you have to detour to build the tools and expect to throw some of them out after you’ve finished using them.

This **approach—automation**, **rapid prototyping**, **incremental iteration**, being friendly to **experimentation**, and breaking down large projects into manageable **chunks—** sounds remarkably like the Agile and DevOps movements of today. 

In order to loop programs together, we need all programs to use the same input/output interface (**file**, just ordered sequence of bytes).
Can be extended to actual files, channels to another process (Unix socket, `stdin`, `stdout`),  a device driver (say `/dev/audio` or `/dev/lp0`), a socket representing a `TCP` connection, and so on.

\* Standard protocol may not be trivial, like in **Bulletin Board Systems** (BBSs), each system had its own phone number and baud rate configuration

**Take-aways** of Unix Philosophy
- Separation of **logic** and **wiring**, as a result of loose coupling design. You can by default use `stdin` and `stdout` or change to other sources, by it is not a problem for the program. 
-  The input files are normally treated as **immutable**. You can run the commands as often as you want, trying various command-line options, **without** damaging the input files.
- You can end the pipeline at any point, pipe the output into `less`, and look at it to see if it has the expected form. This ability to inspect is great for **debugging**.
- You can write the output of one pipeline stage to a file and use that file as input to the next stage. This allows you to restart the later stage without rerunning the entire pipeline.

---

### MapReduce

The idea is similar to the Unix tools, but **MapReduce** do I/O on distributed filesystem (like **HDFS, Hadoop Distributed File System** and **GFS, Google File System**).
So as **object storage services** like Amazon S3, Azure Blob Storage, and OpenStack Swift.

HDFS follows **shared-nothing** principle, making it not relying on special hardware (store with redundancy for fault tolerance). Consists **daemon process** to expose network service allowing file access. A central server called the **NameNode** keeps track of which file blocks are stored on which machine. 

---

MapReduce algorithm requires 2 callback functions: **mapper** (called once for every input record, generate k-v pairs from input, no state stored) and **reducer** (takes the k-v pair, iterates to produce output).

1. Mapper and reducer can operate only on one record at a time, do not consider related states. 
2. Usually the application codes need to be moved to machines with task assigned first, like with **k8s**.
3. **Hash** of key is used, to put k-v paris with the same key to the same reducer.
4. The reducers are also (author configurably) partitioned.
5. The key-value pairs must be **sorted** (by the mapper, to be performed in stages). After that, the reducers can connect to mappers and download the files of sorted k-v pairs, this is called **shuffling**. For k-v pairs with the same key from different mappers, they will also be merged before parsed by reducers.

It should be noted that **chained MapReduce** is more like a series of command, where each command's output is written to a temporary file (Hadoop writes to disk a lot, even unnecessary).

---

**Reduce-Side Joins and Grouping**: **MapReduce** do not have indexes in usual sense, so it usually do **full table scan** (very expensive). Also, **random-access** request through network is either too slow or too expensive. A better approach may be taking a copy of the database and put it in the same distributed filesystems.

***Example***: You may want to join user activity table with profile table. With such copies in HDFS, you can use map reduce to extrac `(user_id, url)` and `(user_id, date_of_birth)` with different mappers, and reduce them into `(user_id, [url, date_of_birth, ...])`
This can be called **Sort-merge joins**, such tuples containing different fields but with same user_id will be **adjacent**.

**Secondary sort**: sort such that the reducer always sees the record from the user database, followed by the activity events (in timestamp order)

Since the reducer processes all of the records for a particular user ID in one go, it only needs to keep **one** user record in memory at any one time, and it never needs to make any requests over the network. 
This algorithm is known as a **sort-merge join**, since mapper output is sorted by key, from both sides of the join.

By bringing related data together, we separated the **physical** network communication aspects of the computation (getting the data to the right machine) from the **application logic** (processing the data once you have it)

---

**Handling Skew** (e.g., **hotkeys**) can also be important, as MapReduce has to wait till all mappers and reducers to finish in every round.

We can detect hot keys with **sampling**, then let mappers send hotkey related records to **serveral** reducers (rather than one determined by hashing). Note that other inputs need to be **replicated** to all reducers which handle the hotkey as well.
Or if we know the hot keys already, we can store them separately.

Note that such reducers' outputs need to be aggregated.

---

### Map-side Joins
With certain assumption about the input data, **Map-side Joins** may optimize the process (while reduce-side joins need **expensive** sorting, copying and merging)
If we can do that, then we can remove the reducer and have mapper writes into certain files.

1. **Broadcast hash joins**: can be used when joining a large dataset with a small dataset (can fit in memory of each mapper). "Broadcast" reveals that each mapper of a partition of the large input can read the entire small input. An alternative is to store the small join input in a **read-only index** on the **local disk** (so we can handle a bit larger "small" set).
2. **Partitioned hash joins** (**bucketed map joins**): If the inputs to the map-side join are partitioned in the same way, then the hash join approach can be applied to each partition **independently**. E.g., if we want to join the user profile and activity tables, then we can partition based on the last digit of `user_id`, because it works for both tables so that we can process on a smaller subset. 
3. **Map-side merge joins**: If input datasets are not only partitioned in the same way, but also **sorted** based on the same key, then the merge can be done by the mapper.

---

**Application of MapReduce**: build search engine **index** (incremental update will be harder, involves merges segments), **K-V pair** as output (e.g., building dataset or database)

It may **not** be a good practice Allowing MapReduce to write into database server (one record once) directly. Network request is slower, database's performance can be impacted, cannot guarantee "atomicity" / **"clean all-or-nothing"**.

Better solution may be building new databases inside the batch jobs, write it as files to output DIR of distributed Filesystem. Once finished, make these files **immutable** and loaded in bulk into servers to serve **read-only** queries.
If replication went wrong, we can easily switch back to old files.

**Diversity of storage**: Hadoop would first dump data into HDFS, then figure out how to process that. This can make data available more quickly.
This paradigm of worrying about schema later and allow data collection to be speeded up is known as "**data lake**" or "**enterprise data hub**". This makes data interpretation a problem just for consumer. Once it is modeled and formated, it can be imported into **MPP (Massively Parallel Processing)** data warehouse.

---

However, MapReduce still faces severe performance issue in many scenarios and not used as widely, but more methods can be applied on top of Hadoop.

**Fault Tolerance** of MapReduce

Batch processes are **less sensitive** to faults than online systems, as tehy do not immediately affect users and can always be rerun.
Failure of single map / reduce task can be tolerated and can be retried. 
Data is frequently loaded to **disk**, because the data volume is big and for durable storage.
These features makes MapReduce suitable for larger jobs. Retry at the granularity of an **individual task** may help, as rerun the whole task can be expensive.

\* The faults do not happen very frequently, however, batch processing jobs are usually with lower priority and can be terminated (**preempted**). This makes ability to recover valuable so that we can make sue of the "scraps" of computation power.

---
### Improvements On MapReduce

**Materialization**: writing intermediate state into files. 
For complex workflows using a lot of MapReduce jobs, such Materialization can be **wasteful** because we have to wait all preceding jobs to finish, and Mappers are often **redundant** (just read back the file written by Reducers).

**Spark**, **Tez** and **Flink** aim at resolving the above issues, by treating the entire workflow as one job.
They are known as **dataflow engines** as they explicitly model the flow of data through several processing stages.

1. Work by **repeatedly** calling a user-defined function (**operators**) to process one record at a time on a single thread. 
2. They **parallelize** work by partitioning inputs
3. They copy the output of one function over the network to become the input to another function.
4. More **flexible**, not required to take strict roles of map and reduce.

**How Operator Connect To Inputs**: 
- **Repartition and sort** records by key
- Take several inputs and to partition them in the same way, but **skip** the sorting.
- For **broadcast hash joins**, the same output from one operator can be sent to all partitions of the join operator.

**Advantages**: 
1. Expensive work like **sorting** only performed in places where it is actually required.
2. No unnecessary map tasks.
3. All joins and data dependencies in a workflow are explicitly declared, making **locality optimization** possible (e.g., place data producer and consumer tasks in the same node).
4. Can keep intermediate state between operators in **memory** or **local disk**, rather than write to **HDFS**.
5. Operators can start as soon as their input is ready, rather than waiting for the entire preceding stage.
6. Existing JVM can be reused to run new operators.

---

**Fault Tolerance**:

**Spark**, **Flink**, and **Tez** avoid writing intermediate state to HDFS, so they take a different approach to tolerating faults:

If a machine fails and the intermediate state on that machine is lost, it is **recomputed** from other data that is still available 
(a prior **intermediary stage** if possible, or otherwise the **original input data**, which is normally on HDFS).

Framework should track how a given piece of data was computed—which input partitions it used, and which operators were applied to it. 
**Spark**: use **Resilient Distributed Dataset (RDD)** to track the ancestor of data.
**Flink**: checkpoints operator state.

\* It is important that the computation is **deterministic**. It matters especially when some lost data is sent to the downstream operators (so that we ensure there is no **contradictions** between the old and new data).
If it is **non-deterministic**, then downstream operators should be killed as well and rerun. Note that certain programming language may not guarantee any order when iterating over elements, and we should try to use pseudorandom numbers using a **fixed** seed.

\*\* For expensive computation or small output, we can still **materialize** it as a file.

We can tell that the tradeoff is like whether you want to store results in a temporary file, or pass it like a Unix pipe.
It should be noted that **Sorting** operation must be first completed before passing to next operator (Flink tends to **incrementally** pass the output of an operator).

---

### Graphs and Iterative Processing
We may need to look at graphs in batch processing context, e.g. **PageRank** in recommendation engine.

Dataflow engines (Spark, Flink, and Tez) typically arrange the operators in a job as a **directed acyclic graph (DAG)**. 
Many graph algorithms are expressed by **traversing** one edge at a time, joining one vertex with an adjacent vertex in order to propagate information, repeat till some condition is met (**transitive closure**).

Graph can be stored in a distributed filesystem, but the "repeative until done" cannot be expressed in plain **MapReduce**, since it only performs a single pass over the data, but should be implemented in an iterative way (but with very low efficiency, as the entire input dataset will be read though small part of the graph changed).

---

The **Pregel** processing model has been introduced as an optimization of the above method, using **Bulk Synchronous Parallel (BSP).**

One vertex can “send a message” to another vertex, and typically those messages are sent along the edges in a graph.
In each iteration, a function is called for each vertex, passing it **all** the messages that were sent to it (via all the adjacent edges, much like a call to the reducer).
In the Pregel model, a vertex remembers its state in memory from one iteration to the next, so the function only needs to process new incoming messages. 

\* If **no** messages are being sent in some part of the graph, **no** work needs to be done.

\*\* It should be noted that it is hard to partition that vertices are colocated on the same machine, a lot of **cross-machine communication overhead**. Thus we should place such algorithm on **single** machine if possible.




