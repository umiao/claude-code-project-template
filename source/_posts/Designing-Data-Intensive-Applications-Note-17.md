---
title: Designing Data-Intensive-Applications-Note-17
date: 2024-04-27 11:27:31
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on challenges with consensus."
---
Discussion on challenges with consensus.
{% asset_img cover.png DDIA Chapter 17 cover: Consensus and Linearizability %}
<!-- more -->

**Consensus**: Get all nodes to agree on something, e.g., the election of new leader. If two nodes both believe that they are the leader, that situation is called **split brain** which can be prevented by consensus.

**Eventually consistency** / **coverage** is a **weak** guarantee.
**Stronger** consistency guarantee may be possible, but can be less fault-tolerant or with worse performance. 

### Linearizability
Database works as if there is only one replica, no replication lag.
Also known as **atomic consistency**, **strong consistency**, **immediate consistency**, or **external consistency**.
It is a **recency guarantee**, means that we always able to see the latest value written to the database.

Considering that we have a write request to the database, while there are other client requesting the database to get the latest value.
Any read operations that **overlap** in time with the write operation might return either old or new value, because we don’t know whether or not the write has taken effect at the time when the read operation is processed. 
These operations are **concurrent** with the write.

However, that is not yet sufficient to fully describe linearizability: if reads that are concurrent with a write can return either the old or the new value, then readers could see a value **flip** back and forth between the old and the new value several times while a write is going on. That is not what we expect of a system that emulates a **"single"** copy of the data.

In order to enforce **Linearizability**, we have to imagine that for some point in time, the above value **flips** from old value to new value. All subsequent reads must also return the new value, even if the write operations **has not** yet completed.
Also, we can add **compare-and-set** `cas` atomic operator, to make the read-write cycle works correctly. (Before write the value $v_{new}$, we can read the value $v_{old}$ which is previously read). Otherwise, return an **error**.

---

**Solution**: We assume each operator to happen at certain **moment** of time. We place **markers** on these moments, and we require such markers are joined up in a **sequential** order, and the result must be a valid sequence of reads and writes for a register (every read must return the value set by the **most recent** write) (new value should take effect, even the write is **not completed**).

The requirement of **linearizability** is that the lines joining up the operation markers always move forward in time (from left to right), never backward. This requirement ensures the **recency guarantee** we discussed earlier: once a new value has been written or read, all subsequent reads see the value that was written, until it is overwritten again.

It is possible (though computationally **expensive**) to test whether a system’s behavior is linearizable by recording the timings of all requests and responses, and checking whether they can be arranged into a **valid sequential order** 

---

**Linearizability** Versus **Serializability**:

**Serializability** is an isolation property of **transactions**, each may read / write multiple objects. It guarantees that transactions behave the same as if they had executed in some serial order (OK to be different from the order which transactions were actually run)

**Linearizability** is a **recency guarantee** on reads and writes of a register / single object. 

When the above two are provided, it is called **strict serializability** or **strong one-copy serializability** **(strong-1SR)**. 

\* Implementations of **serializability** based on **two-phase locking** (2PL) or **actual serial execution** are typically **linearizable**.
\*\*  Serializable snapshot isolation is not linearizable, because read is made from consistent snapshot, does not include writes that are more recent than the snapshot.

---

One way of electing a leader is to use a **lock**: every node that starts up tries to acquire the lock, and the one that succeeds becomes the leader. The lock must be **linearizable** to reach consensus.

Distributed locking can be used in more granular level, e.g., in  **Oracle Real Application Clusters (RAC)**, lock is on disk page level, with multiple nodes sharing access to the same disk storage system.

**Uniqueness guarantees** is similar to lock (or **compare-and-set**), e.g., to solve naming conflicts. This can also be used to enforce **constraints**, like make sure bank account balance being non-negative, or inventory not below zero.
Such constraints do require linearizability. While foreign key or attribute constraints do not need such property.

---

**Cross-channel timing dependencies**: 

Race conditions may be possible between different channels, without linearizability.
E.g., a server would first store the full size picture and send message to generate a resized picture (**thumbnail**). If the latter is faster, it may receive NULL result, or a old-versioned picture.
This is due to me have two different communication channels between the web server and the resizer: the file storage and the message queue.

--- 

### Implementations of Linearizability
- **Single Replica**: linearizable, but vulnearable to data loss and failure
- **Single-leader replication**: potentially linearizable if you read from the leader or synced followers. However, may not be linearizable due to design (snapshot isolation) or concurrency bugs. However, we need the assumption that everyone knows who is the leader. Otherwise we may have **delusional leader** continues to serve requests.
- **Consensus algorithms**: Linearizable.
- **Multi-leader replication**: Not Linearizable. Because usually the replication is done asynchronously, may need conflict resolution.
- **Leaderless replication**: probably not linearizable. Such **Dynamo style** thing sometimes claimed that you can obtain **strong consistency** by requiring quorum reads and writes ($w + r > n$) but this might not be true.
- **Last write wins** conflict resolution methods based on **time-of-day** clocks are almost certainly **nonlinearizable**, because clock timestamps cannot be guaranteed to be consistent with actual event ordering due to **clock skew**. 
**Sloppy quorums** also ruin any chance of linearizability.

---

We can construct samples that even with quorum reads and writes ($w + r > n$) met, the execution can be **non-linearizable**:

Consider that $n=3, w=3, r=2$, and we have replica A, B and C. First new value is written to replica A, then client X reads A, B to get the new value; Then client Y reads B, C to get the old value.

This is non-linearizable as Y reads after X, but get the older value.

Safest to assume a leaderless system with Dynamo-style replication does **not** provide linearizability.
With reduced performance, we can make it linearizable: a reader must perform **read repair** synchronously, before returning results to the application; a writer must read the latest state of a quorum of nodes before sending its writes.
Also, a linearizable **compare-and-set** operation cannot, because it requires a **consensus** algorithm

---

**The CAP theorem**： If your application requires **linearizability**, and some replicas are disconnected from others, then they must **wait** until the network is fixed, or return an error.
Otherwise (no linearizability needed), we can allow each replica to process requests indenpendently even disconnected (e.g., in a **multi-leader** setting)

\* **CAP** is sometimes presented as **Consistency**, **Availability**, **Partition tolerance**: pick 2 out of 3. 

However, network partition just happens as a kind of fault, and you do not have a choice. When this happens, we can provide either **linearizability** or **total availability**.
CAP cannot help us best understand the system (does not consider network delays, dead nodes, or other trade-offs) and better avoided.

---
Few systems are actually **linearizable** in practice, not even RAM on a modern multi-core CPU, because each core has its own memory **cache** and store **buffer**. Memory access goes to cache by default, then written out to memory **asynchronously**.

Thus, many systems give up providing linearizability, due to performance concern. 
It is prove that if you want linearizability, the response time of read and write requests is at least **proportional** to the uncertainty of delays in the network. However, delays can be long in a network with highly variable delays.

---
### Ordering
**Causality** imposes an ordering on events: cause comes before effect.
Something has to be created before updated, A and B should not have causal link between them to become concurrent. "Consistent" read also means that snapshot should contains answer as well as the question it trying to answer.

If a system obeys the ordering imposed by causality, we say that it is **causally consistent**.

The causal order is not a **total order** (arbitrary two elements can be compared). $\\{a, b\\}$ cannot be compared with $\\{b, c\\}$, being **incomparable** (unless one is subset of another)

In a linearizable system, we have a **total order** of operations.
Therefore, no concurrent operation exists in such system. If there is any, we can only have a **partial order** such that they are incomparable (not causally related).
Linearizability is **stronger** than preserving causality.

**Version control system** like **Git** works as a graph of causal dependencies, where timeline **branches** and **merges**.

**Conclusion**: Causal consistency is the **strongest** possible consistency model that does not slow down due to network delays, and remains available in the face of network failures.
Implementation **causality consistency** requires tracking **causal dependencies** across the entire database, can be done with **version vectors** / **logical clock**.

---

### Noncausal sequence number generator
If there is not a single leader (due to multi-leader / leaderless database), it is less clear about how to generate sequence numbers for operations. Potential solutions:

- Each node generate its own **independent set** of sequence numbers, e.g., only generate multiple of $k$ as version number, or reserve bits in binary representation as unique identifier
- Attach a **timestamp** from a time-of-day clock (e.g., last write win).
-  **Preallocate** blocks of sequence numbers, e.g. (1-1000) just for node A.

However, these methods **cannot** capture the ordering of operations correctly.

### Lamport timestamps
Generating sequence numbers that is consistent with **causality**
Represent timestamp as  ***(counter, node ID)*** so that each timestamp is unique. `counter` is used to determine order, and `node ID` work as tie-breaker.
Every node and every client keeps track of the **maximum** counter value it has seen so far, and includes that maximum on every request. 
When a node receives a request or response with a maximum counter value greater than its own counter value, it immediately **increases** its own counter to that maximum (enforcing the timestamp to be in consistent with the causality).

Difference between **version vectors**: Lamport time‐stamps are more **compact**, but cannot tell whether two operations are concurrent or whether they are causally dependent (**total ordering** is always enforced).

---
### Total order broadcast
It should be noted that Lamport timestamps is not sufficient in some tasks like username creation, because we cannot determine whether concurrent requests are asking for the same name, and which one should win (need knowledge from other nodes). We need not only total ordering of operations, but also when that order is **finalized** (maybe with total **order broadcast**). 

Partitioned databases with a single leader per partition often maintain ordering only **per partition**, which means they cannot offer consistency guarantees (e.g., consistent snapshots, foreign key references) **across partitions**. 

**Total order broadcast** or **Atomic Broadcast**: used to scale the system if the throughput is greater than a single leader can handle, and also how to handle failover if the leader fails.
Usually described as a **protocol** for exchanging messages between nodes. 
Requires: **Reliable delivery** (No messages are lost: if a message is delivered to one node, it is delivered to all nodes.) and **Totally ordered delivery** (Messages are delivered to every node in the same order).

**State machine replication**: If every message represents a write to the database, and every replica processes the same writes in the same order, then the replicas will remain consistent with each other (aside from any temporary replication lag). 

---

An important aspect of total order broadcast is that the order is **fixed** at the time the messages are delivered: a node is not allowed to retroactively insert a message into an earlier position in the order if subsequent messages have already been delivered. 
This fact makes total order broadcast **stronger** than timestamp ordering 

We can view it as a way of creating a log, delivering a message is like appending to the log. 
Since all nodes must deliver the same messages in the same order, all nodes can read the log and see the same sequence of messages.

Total order broadcast is also useful for implementing a **lock** service that provides **fencing tokens**. Every request to acquire the lock is appended as a message to the log, and all messages are sequentially numbered in the order they appear in the log. 
The sequence number can then serve as a fencing
token, because it is monotonically increasing. In ZooKeeper, this sequence number is called **zxid**

---

**Total order broadcast**: **asynchronous**: messages are guaranteed to be delivered reliably in a **fixed order**, but there is no guarantee about **when** a message will be delivered
**Equivalent** to **consensus**.

**linearizability**: **Recency guarantee**: a read is guaranteed to see the latest value written.

We can try to use **Total order broadcast** to implement a **linearizable storage** to resolve the username setting task:
1. Append a message to the log, decalring the name you want to claim
2. Read the log, wait for the message you appended to be delivered back to you.
3. Check for any messages claiming the user name you want; If the first is your own message, then it is succesful, otherwise it is claimed by others.

This is like a compare-and-set, each name initially with value `NULL` and you want to assigny your userID as value of the name. It is only legal to overwrite name with value `NULL`

---

1. Because log entries are delivered to all nodes in the same order, if there are several **concurrent** writes, all nodes will **agree** on which one came first. 
2. Choosing the first of the conflicting writes as the winner and aborting later ones ensures that all nodes agree on whether a write was committed or aborted. A similar approach can be used to implement **serializable multi-object transactions** on top of a log.
3. Ensures linearizable writes, not **linearizable reads**. Data read from a store which is asynchronously updated from the log can be stale (this procedure provides **sequential consistency** / **timeline consistency**, slightly weaker than linearizability).



To make reads linearizable:
1. Append a message to a log, read the log, performing the actual read when the message is delivered back to you so reads can be sequenced.
2. If the log allows you to fetch the position of the latest log message in a linearizable way, you can query that position, wait for all entries up to that position to be delivered to you, and then perform the read. (ZooKeepter's `sync()` operation)
3. Read from a replica that is **synchronously** updated on writes,
and is thus sure to be up to date. 

---

We can also build **total order broadcast** from **linearizable storage**.
With a **linearizable register** (or atomic compare-and-set), you can increment and get the linearizable integer, and attach it in the message as sequence number. You can then send the message to all nodes (resend lost messages) and the recipents will deliver the messages consecutively.
Unlinke Lamport timestamps, the numbers must form sequence with **no gaps**, making it total order (you will know that you should wait for No.5 messages even you received No.4 and No.6). 

In order to restore the register value when network connections fails, you inevitably get a **consensus** algorithm.
Linearizable **compare-and-set** (or **increment-and-get**) register and **total order broadcast** are both equivalent to **consensus**

---

- **Consesus** is important in **leader election** (of database with single-leader replication) and **Atomic commit** (in database cross nodes or partitions).

**FPL** result: No algorithm can reach consensus with risk that a node may crash, in async system model and no clock and timeout is allowed.

With **timeouts** or other methods (even use of random numbers) to detect crashed nodes, then consensus is solvable.

### Atomic Commit and Two-Phase Commit (2PC)
Atomicity prevents failed transactions from littering the database, and makes sure **secondary index** stays consistent with the primary data.

For **single** node, a database usually makes the transaction's write durable (writeahead log, e.g.) then append a commit record to the log on disk (2 phase commit). If node is crashed before commit record is written, then the writes are **rolled back**.

For **multiple** nodes, we need to ensure all nodes either commit or abort. It is **not** allowed that some commit succeed and some fail.
Once committed, a commit is **irrevocable**.
However, we can undo a commit by another independent one: **compensating transaction**.

---

**Implementation**:
**2PC** introduces a **coordinator** (also known as **transaction manager**) to arrange the commit on all nodes.
In 1st phase: Coordinator send request to all nodes and ask if they are able to commit. If anyone responses "no", then coordinator sends an **abort** request to all nodes.
In 2nd phase: Coordinator send commit request, and commit actually takes place (and broadcasted).

---

**Details** of 2PC implementation:
1. Before begin a distributed transaction, application needs to request a **globally unique** transaction ID.
2. The application begins a **single-node** transaction on each of the participants (to do all reads and writes), and attaches the globally unique transaction ID. If anything go wrong, coordinator or any participant can abort.
3. The coordinator sends a **prepare request** to all participants, tagged with the global transaction ID, when the application is ready to commit. If any request fails / times out, the coordinator sends an abort request for that transaction ID to all nodes.
4. When a participant receives the prepare request, it makes sure that it can definitely commit the transaction under **all** circumstances. This includes writing all transaction data to disk (a crash, a power failure, or running out of disk space is **not** an acceptable excuse for refusing to commit later), and checking for any conflicts or constraint violations. By replying “yes” to the coordinator, the node promises to commit the transaction without error if requested. In other words, the participant **surrenders the right to abort** the transaction, but without actually
committing it.
5. When the coordinator has received responses to all prepare requests, it makes a **definitive decision** on whether to commit or abort the transaction (committing only if all participants voted “yes”). The coordinator must write that decision to its transaction log on disk so that it knows which way it decided in case it subsequently crashes. This is called the **commit point**.
6. Once the coordinator’s decision has been written to disk, the commit or abort request is sent to all participants. If this request fails or times out, the coordinator **must retry forever** until it succeeds. There is no more going back: if the decision was to commit, that decision must be enforced, no matter how many retries it takes. If a participant has crashed in the meantime, the transaction will be committed when it recovers—since the participant voted “yes,” it cannot refuse to commit when it recovers.

Thus, the protocol contains two crucial “**points of no return**”: when a participant votes “yes,” it promises that it will definitely be able to commit later (although the coordinator may still choose to abort); and once the coordinator decides, that decision is **irrevocable**. 
Those promises ensure the **atomicity of 2PC**. 
(Single-node atomic commit lumps these two events into one: writing the commit record to the transaction log.)

---

**Coordinator failure**: 
If one of participant's **prepare requests** fail or time out, coordinator aborts the transaction.
if any of the **commit** or **abort** requests fail, the coordinator retries them **indefinitely** (that is why **2PC** is called **blocking** atomic commit protocol).

However, if coordinator failed, participants's state is called **in doubt** or **uncertain**, as they have to wait forever (cannot abort).
In **2PC** protocol, the only way is to wait coordinator to **recover**.

The commit point of 2PC comes down to a regular **single-node atomic commit** on the coordinator.

---

**3PC** is proposed to make an atomic commit protocol **nonblocking**, but we need assumption that having a network with **bounded** delay and nodes with **bounded** response times.
However, in a system without such assumption, **3PC** cannot guarantee atomicity (without a **perfect** failure detector)
That is why **2PC** is still in use

---

### Heterogeneous distributed transactions

**Database-internal** distributed transactions are easier to deal with, like distributed databases. All nodes (participants) run the **same** database software. They do not have to be compatible with other system, able to use any protocol and do specific optimization.

**Heterogeneous** distributed transactions are harder, e.g., message brokers. Atomic commit **must** be ensured.

**Exactly-once message processing**:  A message from a message queue can be acknowledged as processed if and only if the database transaction for processing the message was successfully committed 
(**atomically** commit the message acknowledgment and database writes in a **single** transaction).
E.g., when a message processing is associlated with sending an email. If either one failed, we can roll back both and safely retry.

### XA transactions
**X/Open XA** (short for **eXtended Architecture**) is a standard for implementing twophase commit across heterogeneous technologies。
The essence is **C API** for interfacing with a transaction coordinator.
Assumes that your application uses a network driver or client library to communicate with other participants / services. If driver supports XA, then it calls the XA API to figure out if an operation is part of a distributed transaction, if so, sends necessary information to the database server. Driver also exposes **callbacks** through which the coordinatro can ask the participant to prepare, commit or abort.

The transaction **coordinator** implements the XA API. 
However, corrdinator is usually just a **library** loaded into the same process as the application issuing the transaction rather than a seperate service.
This is bit tricky as coordinator can go with died server.

---

The reason that we really care about transaction in **doubt** is that they might be holding locks (if any **exlusive** lock or **2PL** is used).
These locks will be holded until coordinator recovers.

In practice, **orphaned in-doubt transactions** do occur.
Coordinator cannot decide their outcome for whatever reason (transaction log may be lost or corrupted). They will sit forever in the database, hold locks and block other transactions.

Only solution is for an administrator to **manually** decide whether to commit or roll back the transactions (a lot of work, and breaks the **2PC** constraints)

XA implementation may have emergency escape hatch called **heuristic decisions**: allowing a participant to **unilaterally** decide to abort or commit an in-doubt transaction without a definitive decision from the coordinator. 

Heuristic here is a euphemism for probably breaking atomicity, since it violates the system of promises in two-phase commit. 
Thus, heuristic decisions are intended only for getting out of **catastrophic situations**, and not for regular use.

---

### Limitations of distributed transactions
1. Limitation of **XA**: transaction coordinator is itself a kind of database (in which transaction outcomes are stored)
If it runs on only one single machine, it is a **single point** of failure and do not even have high availability.
2. Many server-side applications are developed in a **stateless** model. Coordinator’s logs will break such model.
3. XA is a **lowest common denominator**, to be compatible with a wide range of data system. Cannot detect deadlocks across different systems (requiring knowledge on locks), does not work with **Serializable Snapshot Isolation**, SSI (require protocol to identify conflicts across different systems). 

Even for **internal** distributed transactions, where we can implement SSI, failures can still be amplified by **2PC** as we require all participants to respond.

---

### Fault-Tolerant Consensus
Some properties we need consensus to have:
1. **Uniform agreement**: No two nodes decide differently.
2. **Integrity**: No node decides twice.
3. **Validity**: If a node decides value v, then v was proposed by some node.
4. **Termination**: Every node that does not crash eventually decides some value (usually, a majority is required as the **quorum**).

The idea is that everyone decides on the same outcome, and once you have decided, you cannot change your mind.
Having a dictator can resolve most properties (except termination), but lacks **fault tolerance**.
In fact, the termination property requires that a consensus algorithm must **make progress**.
Any algorithm that has to wait for a node (like **2PC**) will NOT have the termination property.

\* It is possible to make consensus robust against **Byzantine faults** as long as fewer than **one-third** of the nodes are Byzantine-faulty

---

The best-known fault-tolerant consensus algorithms are **Viewstamped Replication** (VSR), **Paxos**, **Raft** and **Zab**.

They decide on a sequence of values, which makes them **total order broadcast** algorithms. 
Remember that total order broadcast requires messages to be delivered **exactly once**, in the **same order**, to **all** nodes. This is equivalent to repeated rounds of **consensus** (decide what to send next, and decide on the next message to be delivered in total order)
Total order broadcast is more efficient than doing multiple **value-at-a-time consensus**.

---

### Epoch numbering and quorums
Consensus protocols internally uses a leader, but leader is a result of **consensus**. Such protocols do not guarantee that the leader is unique.

We can make a weaker guarantee with **epoch numbering** (**ballot number / view number / term number**), and guarantee that within each epoch, the leader is unique. Every time the current leader is thought to be dead, a vote is started among the nodes to elect a new leader.

 This election is given an **incremented** epoch number, and thus
epoch numbers are **totally ordered** and **monotonically increasing**. 

1. If there is a conflict between two different leaders in two different epochs (perhaps because the previous leader actually wasn’t dead after all), then the leader with the **higher** epoch number prevails (so we remove the previous leader even it recovers).
2. For every decision that a leader wants to make, it must send the proposed value to the other nodes and wait for a **quorum** (usually a majority of nodes) of nodes to respond in favor of the proposal.
3. A node votes in favor of a proposal only if it is **not aware** of any other leader with a higher epoch.
4. Have two rounds of voting: once to choose a **leader**, and a second time to vote on a leader’s **proposal**. The key insight is that the quorums for those two votes must *overlap*: if a vote on a proposal succeeds, at least one of the nodes that voted for it must have also participated in the most recent leader election. 
5. The leader got to know if it is still holds the leadership.
6. Consensus algorithms define a **recovery process** by which nodes can get into a consistent state after a new leader is elected, ensuring that the safety properties are always met.

**Limitations of Consensus**: 
- Vote on proposal is actually **synchronous** replication, and can result in data loss.
- Needs **strict majority** to operate. Most consensus algorithms assume a **fixed** set of nodes participate in voting, means you cannot just add / remove nodes in the cluster (may be resolved by dynamic membership).
- **Sensitive** to network problems, relies on timeout for failure detection.

---

Consesus Algorithm Projects like ZooKeepter are very useful for **distributed coordination**. It is limited as it can only hold small amount of data able to fit in memory, and replicated across all node using **fault tolerant total order broadcast** (also **Linearizable atomic operations** are implemented to implement lock).

**Failure detection**: Clients maintain and long-lived session on ZooKeeper servers to exchange **heartbeats**, if it cease for longer than the session timeout, session is declared to be dead and locks are released (ZooKeeper calls these **ephemeral nodes**).

**Change notifications**:  One client read locks and values that were created by another client, and can also watch them for changes. Then it can know if a client joins the cluster or fails, without frequently **poll** to find out.

Only the linearizable atomic operations really require consensus.

**Use Cases**: **ZooKeeper** can be used for **leader election**, **partition assigning**, **rebalancing** and taking over **failed** node's work (maybe even service discovery). It runs on fixed number of nodes, performs its majority votes among them and supports potentially large number of clients. Normally, the kind of data managed by ZooKeeper is quite **slow-changing** (not suitable to store runtime state of application)













