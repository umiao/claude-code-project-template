---
title: Designing Data-Intensive-Applications-Note-16
date: 2024-04-21 09:54:34
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on challenges with distributed systems."
key_concepts:
  - Fault Tolerance
  - Consistency
  - Split Brain
  - CAP Theorem
takeaways:
  - Use fencing tokens to prevent split-brain scenarios when a leader's lease expires
  - Prefer logical clocks over wall clocks for ordering events in distributed systems
  - Design for partial failures by assuming any network message can be lost, delayed, or duplicated
  - Apply the Phi Accrual failure detector for adaptive timeout-based node failure detection
series: DDIA
series_index: 16
---
Discussion on challenges with distributed systems.
<!-- {% asset_img cover.png DDIA Chapter 16 cover: Challenges in Distributed Systems %} -->
<!-- more -->

### Faults and Partial Failure
We expect outcomes of program running on a single computer either returns correct result, or crash (without returning wrong results)
**Idealized system model**: operates with perfection, **CPU instruction** does the same thing, data in **memory and disk** remains intact and not randomly corrupted.

However, in distributed system, we can easily find **partial failure** that some parts of the system that are broken in unpredicatable ways but remaining parts working fine.
You may not even know if something succeeded or not, as the time it takes for message traveling across netowrk is **nondeterministic**


Large-scale computing systems' design logic is between **High-performance Computing (HPC)** and **Cloud Computing**. 

The prior is more like a single node computer (if failure happens, fix it and restart entire cluster workload from checkpoint [can be expensive]]). Also, it has node communication through shared memory and **Remote Direct Momoery Acess (RDMA)**, use specialized hardware and more reliable. Also, having its nodes close together.

The latter focuses on high availability, based on IP and Ethernet, arranged in Clos topologies to provide high bisection bandwidth.
System with fault tolerance can do things like **rolling upgrade**, or kill-n-restart virtual node.

---

**Fault Tolerance**: It is important to consider wide range of possible faults, even fairly unlikely ones. Fault handling mech should be part of the software design.

You can construct a more reoliable system from a less reliable underlying base. E.g., using **error-correcting** codes to detect random bit error during transmission, and use **Transmission Control Protocol** (TCP) to form more reliable transport layter on top of IP (**Internet Protocol**)
However, these methods have their own limit of how much error can be detected and handled, and TCP cannot resolve network latency issue.

---

**Unreliable Network**: Usually, one node can send a message / packet to another node, but there is **no guarantee** when it will arrive, or whether it will arrive at all.
Sender cannot tell if the packet was delivered, because recipent's response message can be lost. Usual way of handling this is setting a **timeout**.
\* Redundancy in data center setting cannot prevent **human error**, which is a main reason for outage.

**Detecting Faults**: Many systems need to detect faulty nodes, e.g., load balancer stop sending request to dead node, and new leader may need to be elected in single-leader setting database. 
However, it is still hard to get response, or get to know how much data is processed before failure happened. If node's operating system is still running, another node may be able to take over.

---

### Timeout and Unbounded Delays
1. **Timeout** can be the only sure way of detecting a fault, but the limit is hard to set.
2. Falsely declaring a **node dead** is problematic, may ended up performing actions twice. Also, extra load would be placed on other nodes, and cause **cascading failure** (extremely all nodes can be declared dead and stop working).
3. If delivery time is bounded by $d$ and request processing time is bounded by $r$, then we can set timeout limit as $2d+r$. Unfortunately, most systems have **unbounded delays**.

**Network Congestion**: Multiple different nodes **simultaneously** try to send packets to the **same destination**, the network switch must queue them up and feed them into the destination network link one by one. Then packet may need to wait for a slot.
\* Packet may be dropped if switch queue is full.

Also, even a packet reaches the destination machine, we may still need to be queued by the **operating system** if the system is busy, or need to wait to get a CPU core in a **virtualized** environment.
**TCP** performs **flow control** (also known as **congestion avoidance** or **backpressure**), in which a node limits its own rate of sending in order to avoid overloading a network link or the receiving node (additional queueing will be needed). 

\* **TCP** would consider a packet to be lost if it is not acknowledged within the timeout. Application will not see the loss and retreansmission, but will see the latency.

**TCP v.s. UDP**: In **latency-sensitive** application, like video conferencing, use UDP rather than TCP because delayed data will be worthless. UDP does **not** perform flow control and does not retransmit loss packets. Human can ask for retransmission instead.

**Determine timeout**: Queueing delays have especially wide range when a system is close to its max capacity and long queue can be built.
You can only choose timeouts **experimentally** to learn the distribution of expected **variability of delays**.

More ideally, systems can continually measure response times and their variability (**jitter**), and automatically **adjust** timeouts according to the observed response time distribution. 
This can be done with a **Phi Accrual failure detector**

### Phi Accural Failure Detector
Traditionally, we can use **heartbeat** for failure detector. Rather than setting the heartbeat timeout to a **constant** value, we assume the heartbeat message matches certain type of probability model. E.g., the interval obeys the normal distribution. 
Then, we can use the history data in the **sliding window**, to estimate the probability parameters with **maximum likelihood** estimation and calculates the probability of receiving heartbeat message at this moment.

- If the node is invalid, we want the $\lim_{t \rightarrow \infty}\phi(t)=\infty$
- $\exists t_0$ such that $\forall x_1 \ge x_2 \ge t_0, \phi(x_1) \ge \phi(x_2)$.
- If the node is valid, then $\phi(t)$ is bounded.
- If the node is valid, then $\exists t_0$ such that $\forall x \ge t_0, \phi(x) =0$.

$\phi(t_{now})$ is defined as $-\log_{10}(P_{later} (t_{now} - T_{last}) )$
$P_{later} (t) = \frac{1}{\sigma \sqrt{2 \pi}} \int_t^{+\infty} e^{-\frac{(x-\mu)^2}{2\sigma ^2}}dx $

Here, $\mu$ and $\sigma$ can be estimated with the data in the **sampling window**.

Each node / subprocess can use their own threshold to compare with (other node's) $\phi(t)$ shared by the failure detector.

---
\* When you make a call over the **telephone network**, it would establish a **fixed**, **guaranteed** amount of bandwidth through the entire route between callers.
 This kind of network is **synchronous**: even as data passes through several routers, it does not suffer from queueing, because the 16 bits of space for the call have already been reserved in the **next hop** of the network. And because there is no queueing, the maximum end-to-end latency of the network is fixed. We call this a **bounded delay**.

The packets of a TCP connection **opportunistically** use whatever network bandwidth is available. 
They are **packet switching**, instead of **circuit-switched** networks, as they are optimized for **bursty traffic**. It can be hard to **guess** a proper bandwidth allocation. TCP can adapt the rate **dynamically**.

**Static** resource allocation can provide **latency guarantees**, but at the cost of **reduced utilization**.

---

### Unreliable Clocks

Usually each machine has its own clock, which makes determining the **order** difficult in case of concurrency.
This makes figuring request **timeout** / getting **timestamps** / scheduling services... more challenging.

We can **synchronize** clocks to some degree with **Network Time Protocol (NTP)**.
NTP uses **hierarchical**, **semi-layered** system of time sources. Each level of hierachy is termerd a **stratum**, assigned with a number starting from 0. A server synchronized to a stratum $n$ server runs at stratum $n+1$. 
\* Stratum is **not** always an indication of quality or reliability

- Stratum 0: High-precision timekeeping devices such as **atomic clocks**, **GNSS** (including GPS) or other radio clocks,
- Stratum 1: Synced within a few microseconds of stratum 0 devices. 
- Stratum 2: Synced with the above level.

The NTP algorithms on each computer interact to construct a **Bellman–Ford** shortest-path spanning tree, to minimize the accumulated round-trip delay to the stratum 1 servers for all the clients.

The **upper limit** for stratum is 15; stratum 16 is used to indicate that a device is **unsynchronized**

**Example**: We will have 4 timestamps $T_1, ... T_4$. Here, client send a request on $T_1$, it reaches the server on $T_2$, response is sent on $T_3$ and arrives on $T_4$.
We can estimate $delay = \frac{T_4 - T_1 - (T_3 - T_2)}{2}$, and the offset satisfies: $\text{offset} + T_4 = T_3 + \text{delay}$, so we can figure out the offset and adjust the clock.

---

Modern computers have at least 2 kinds of clocks: a **time-of-day clock** (returns date and time according to some calendar, known as **wall-clock time**, like seconds since the epoch:midnight on 1st Jan 1970, might jump back) and a **monotonic clock** (for measuring a **duration**, never jumps back, the unit might be in nano-seconds).

**NTP** may adjust the frequency at which the monotonic clock moves forward, if the local quartz is moving faster or slower (allow error up to 0.05%). Such error is tolerable in distributed systems.

There lies some challenges in getting the clock synchronized:
1. Quartz clock in a computer can **drift**, depending on the temperature. It may be a 17 seconds drift for a clock resynchronized once a day.
2. Local clock may refure to synchronize if it differs too much from an **NTP** server, or local clock be forcibly reset.
3. **NTP** synchronization can only be as good as the network delay. Itself may go wrong as well.
4. **Leap seconds** result in a minute has 59 / 61 seconds. NTP server can perform the leap second adjustment gradually over the course of a day (called **smearing**)
5. Hardware clock can be virtualized in virtual machines, and each VM can **pause** for tens of miliseconds and clock jumps forward.
6. You cannot trust user device's clock setting.

Inaccurate clock can casue lost of updates, under setting of **Last Write Wins**. 
A node with **lagging** clock cannot overwrite values previously written by a node with a **fast** clock, casuing data be **silently** dropped. 
**LWW** cannot distinguish truly **concurrent** writes (writes are not aware of each other) and writes that occurred **sequentially** in quick succession (writers are aware of others).
Clock reading should be viewed as a range within a **confidence interval**, rather than a point in time.

We may need **tie breaker**, if two nodes generate the same timestamp.
**Logical clocks** based on **incrementing counters** may be a better solution, only measuring the relative ordering of events.

---

### Synchronized clocks for global snapshots

The most common implementation of snapshot isolation requires a **monotonically increasing** transaction ID. 
On single node, this can be generated by a counter. 
However, it is challenging for database distributed across many machines / data centers, because transaction ID must reflect **causality**, but we have **clock accuracy** concern. 

1. **TrueTime API** can report clock's **confidence interval**, and we can use it to determine if two time reading overlap.
2. We can wait the length of the confidence interval before committing a **read-write** transaction.
Above is used in **Google** only

---

### Process Pauses
In single leader setting database, leader has to know if it is **not** declared by others and safely accept writes.
one options is let leader obtain a **lease** from other nodes, which is similar to a lock with a timeout. If the leader dies, it will not renew the lease and another node can take over.

However, if we want to use a timer in the implementation, we will have the clock issue (if different nodes' clocks go out-of-sync).

Even we use a **local monotinic clock**, it is still possible that an **unexpected pause** happens after the leader checked that it still hold the lease. Another node may become the leader during this time, but the old leader is not aware of that.

**Potential Reasons of such pause**:
1. (Stop the world) **Garbage Collection**, may stop all running threads. [One emerging idea is to treat **GC** pause like brief planned outages of a node, used in some **latency-sensitive** financial trading systems]
2. Suspended **virtual machine** (to migrate to another node, for example).
3. In end-user devices like latops, execution can be suspended.
4. **Context Switch** between threads or virtual machines. CPU time spent in other virtual machines is known as **steal time**.
5. Slow **I/O**, or delay caused by **paging** (swaping to disk). Servers can disable paging to avoid **thrashing** (spend most of the time swapping pages)

You can’t assume anything about timing, because arbitrary **context switches** and **parallelism** may occur (just like making multi-threaded code).
For distributed systems, we do not have tools like **mutexes**, **semaphores**, **atomic counters**, **lock-free** data structures, **blocking queues**, and so on.

---

**Response time guarantees**: In some systems (like rocket, called **hard real-time systems**), we have a deadline by which the software **must** respond. 

In **embedded systems**, real-time means that a system is carefully designed and tested to meet specified **timing guarantees** in all circumstances.
In **network**, real-time means servers pushing data to clients and stream processing without hard response time constraints

Providing real-time guarantees in a systems can be challenging, as it requires: a **real-time operating system** (RTOS) that allows processes to be scheduled with a guaranteed allocation of CPU time in specified intervals is needed; library functions must document their **worst-case** execution times; dynamic memory allocation may be **restricted** or disallowed entirely (real-time garbage collectors exist, but the application must still ensure that it doesn’t give the GC too much work to do); and an enormous amount of testing and measurement must be done.

---
It should be noted that even if a node believes that it is leader (or hold the lease, etc), that doesn’t necessarily mean a **quorum** of nodes agrees! 
\* We should not do the validation only on application end. We need the resource / data itself in checking tokens.

**Fencing**: Every time the lock server grants a lock or lease, it also returns a **fencing token**, which is a number that increases every time a lock is granted (e.g., incremented by the lock service). We can then require that every time a client sends a write request to the storage service, it must **include** its current fencing token.
If server ever processed a write with a higher token number, it rejects the write with old token.

If **ZooKeeper** is used as lock service, the transaction ID **zxid** or the node version **cversion** can be used as fencing token. Since they are guaranteed to be **monotonically increasing**

### Byzantine Faults
Fencing tokens can work well (with **honest** but **unreliable** assumption). However, if it is not honest, it could fake such token and cause **Byzantine fault** (reaching **consensus** in this **untrusting** environment).

The problem needs $n$ generals who need to agree, but we have some traitors among them sending fake messages.
A system is **Byzantine fault-tolerant** if it can tolerate nodes which are **malfunctioning** and **not** obeying the protocol, or if **malicious** attackers are interfering with the network.

We can safely assume there is no Byzantine fault in most datacenters / databases. Such solution can be complicated ted and need support from hardware level.
Usually, the server has **central authority** to determine what kind of behavior is allowed and do protection with **authentication**, **access control**, **encryption**, **firewalls**, and so on. 

Also, if you deploy same software to all nodes, **Byzantine fault-tolerant algorithm** may not help, because we expect the error to be independent so that we can some nodes functioning correctly.

---
### Timing Assumption Model
1. **Synchronous model**: bounded network delay, bounded process pauses,
and bounded clock error. Not very realistic as unbounded delays can occur.
2. **Partially synchronous model**: Behaves like a synchronous system most of the time, but exceeds the bounds sometimes. 
3. **Asynchronous model**: No any timing assumptions, not even have a clock.

Common Models of **System (Node) Failure**:
1. **Crash-stop faults**: Only crash may happen, then the node gone forever.
2. **Crash-recovery faults**: May recover after sometime if crashed. Nodes are assumed to have **stable storage** (i.e., non-volatile disk storage), while the **in-memory** state is assumed to be lost. Usually most useful.
3. **Byzantine (arbitrary) faults**: Node can do anything, including being **dishonest**

---

We may be interested in the following properties under the above failure models:

1. **Correctness**: We can write down the properties we want a distributed algorithm to have, to define correctness.
2. **Safety and liveness**: Usually we can distinguish **liveness** properties from **safety** properties, as prior usually include the word "eventually" in their definition. Safety means nothing bad happens, but liveness means something good eventually happens.
3. **Formal Definition**: If **safety** property is viloated, we can point out a particular time at which it was broken, and such violation cannot be undone. For **liveness** property, it may not hold at some point in time, but there is always hope that it may be satisfied in the future.

For distributed algorithms, it is common to require safety properties always hold (to ensure it does not return a **wrong** result in terms of failure). For liveness properties, we can make caveats and state that only if majority of nodes have not crashed, we can say a request needs to receive a response.























