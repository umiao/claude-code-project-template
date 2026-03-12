---
title: Designing Data-Intensive-Applications-Note-19 [END]
date: 2024-05-06 14:51:50
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on challenges with stream processing."
key_concepts:
  - Stream Processing
  - Change Data Capture
  - Message Queues
  - Fault Tolerance
takeaways:
  - Use log-based message brokers like Kafka when consumers need to replay messages or maintain ordering
  - Apply change data capture to keep derived data systems in sync with the source database
  - Choose the right window type (tumbling, hopping, sliding, session) based on your aggregation semantics
  - Achieve exactly-once semantics through idempotent operations rather than relying on transaction guarantees
series: DDIA
series_index: 19
---
Discussion on challenges with stream processing.
{% asset_img cover.png DDIA Chapter 19 cover: Stream Processing %}
<!-- more -->

### Stream Processing

Generalization of batch processing, which removes the assumption that the input is **bounded** of a known and **finite** size.

Daily batch processes may be too slow to reflect chagnes, that is why we can process data continuously, abandoning the fixed time slices entirely and simply processing every event as it happens. That is the idea behind **stream processing**.

**Stream**: data that is incrementally made available over time.

**Event**: A small, self-contained, **immutable** object containing the details of something that happened at some point in time. 
An event usually contains a **timestamp**, and may be encoded as a text string, JSON or in binary form.

In streaming terminology, an event is generated once by a **producer** (also known as a **publisher** or **sender**), and then potentially processed by multiple **consumers** (**subscribers** or **recipients**)
Related events are usually grouped together into a topic or stream.
In case of **continual** processing with **low** delays, **polling** can be expensive without special optimization.
Lower the percentage of requests can return new events, and make the overhead high. 

---

Instead, it is better for consumers to be **notified** when new events appear (cannot be handled well by traditional DB).
A common solution is to use **Messaging Systems** (a producer sends a message containing the event, which is then pushed to consumers).
\* Unix pipe and TCP connection are easy way to implement, but usually it is extended so that multiple producers / consumers are allowed to send / receive.

1. In case producers send messages **faster** than the consumers can process them: **drop** message, store in **queue** or apply **backpressure** (a.k.a **flow control**, block the producer from sending more messages) [we can have a small fixed-size buffer, block sender if filled up].
2. In case node **crashes** or **temporarily** go **offline**. Note that **durability** comes with cost of performance, and should be determined by need of application.

**Direct messaging methods**:
1.  **UDP multicast**: low latency, unreliable, retransmit on demand
2. Brokerless messaging libraries such as **ZeroMQ** and **nanomsg** take a similar approach, implementing publish/subscribe messaging over **TCP** or **IP** multicast.
3. Or we can use unreliable UDP messaging for collecting metrics (like **counter**) from all machines on the network and monitoring them.
4. Consumer can expose service on network, producers can make direct **HTTP** or **PRC** request to push messages to the consumer.  A **callback URL** of one service is registered with another service, and it makes a request to that URL whenever an event occurs. (The idea of **webhooks**)
5. However, we usually assume producer and consumers are constantly **online**. Otherwise, consumer can miss messages from producer if offline. 

---

### Message Brokers
Also known as **message queue**, a kind of database optimized for handling **message streams** (consumers and producers connect as clients, read and write from the broker).

Clients can come and go, **durability** is handled by the broker. **Unbounded** queueing can be allowed.

The consuming is also **asynchronous**: producer will not wait till the message got consumed.

**Difference with Database**:
1. Delivered message will be deleted.
2. Will assume the working set to be small, the queue is **short**, can overflow to **disk**.
3. Rather than secondary indexes, brokers usually support **subscribing** to a **subset** of topics matching some pattern.
4. Do not support arbitrary queries (based on **snapshot isolation**), will notify clients when data changes.

When serving **multiple** consumers, we can either do **Load balancing** (each message is delivered to one of the consumers, for them to share the work of processing) or **Fan-out** (each message is delivered to all consumers).
These patterns can be combined to be used.

**Acknowledge** from client is needed before deleting a message, otherwise it is **redelivered** to another consumer (**atomic commit protocol** is needed in case message is processed by lost in network).
\* Note that combination of load balancing with redelivery inevitably leads to messages being **reordered**. If there are causal dependencies between messages, do not use load balancing.

Messages stored in broker are regarded as temporary, and the acknowledgement is **destructive** as discussed above.

---

**Log based** message brokers aims at achieving low-latency notification and durability. 
Producers append message to end of log, consumers read log sequentially, if it reaches the end, waits for the notification of a new message appended. (just like `tail -f` in unix)
Log can be partitioned on different machines by different topics, and achieve higher **throughput**.
Within each partition, each message has a **monotonically** increasing sequence number, or **offset** and messages are **totally ordered**. **No** ordering guarantee across different partitions
Examples: **Apache Kafka**, **Amazon Kinesis Streams**, and Twitter’s **DistributedLog**

Log based method usually supports **fan-out** messaging, as consumers can independently read the log. 
Load balancing can be done on partition level (**coarse grained**), and consumer read partition using **single-threaded** manner.

**Limitations**: 
1. The number of nodes sharing the work of consuming a topic can be **at most** the number of log partitions in that topic.
2. Single slow message can hold the processing of subsequent messages in the same partition.

Consumer can maintain an **offset** to record which messages have been processed. In case of consumer failure, another node and restart from this offset.
Also, **"append-only"** log makes **replaying** and **recovering** easier.

---

**Disk Usage** of Log Based Broker:
To reclaim disk space, the log is divided into **segments** and old segments can be deleted or moved to archieve storage.
It is possible that a slow consumer fall behind and its consumer offset points to a deleted segments and miss some messages.

Effectively, the log implements a **bounded-size buffer** that discards old messages when it gets full, also known as a **circular buffer** or **ring buffer** (the size can be large).
After the buffer is filled, old messages start to be overwritten.

Each message will be written to disk anyway, making the throughput more **constant** (and relatively higher) than memory-disk based broker.

---

### Stream Data Systems
In practice, multiple technoligies can be used in applications (e.g., OLTP database, cache, index, data warehouse..).
Each has its own copy of data in different representation, so they need to be kept **in sync** with each other.

**Dual writes** (explicitly writes to **each** of the systems when data changes) are used in case periodic full database dumps are too slow.
However, it is prone to **race conditions**, the eventual result on each system may not be consistent (due to the order certain message arrives). Also, some write may fail.
We can use **2PC** to solve, but with high cost.

---

**Change Data Capture** has become an interesting topic, where we can take changes made in a database and replicate them to different storage technology like indexes or caches.
This can be hard, because there is a lot of internal implementation details of databased exposed in log.

**Implementation**: 
We can make one database the leader and others as followers using log based message broker (without reordering issue).
Log consumers are **derived** data systems, just storing another **view** on the data and we ensure all changes also reflects in the derived data systems.
\* Database trigger can be used, but with poor performance.

Keep all the changes log for replay can be expensive, so we can have it **truncated** and create an **initial snapshot**.
Snapshot must correspond to a known **position** or **offset** in the change log.

**Log Compaction**: logs can be compacted by discarding duplicates, merge by key and only the latest value is preserved. Deleted keys (indicated by **tombstone**) would also be removed.
\* This idea can be extended to log-based message brokers and change data capture, where we only keep the **most recent** write for a particular key.
When rebuilding data system, we can just start scaning from the beginning of a compacted log, without taking another snapshot of the CDC source database.

---

**Event Sourcing**: store all changes to the application state as a log of change events.

For **Change Data Capture**, the application uses the database in a **mutable** way (also a low level way, like parsing change logs), and application writing to DB does not need to be aware of it.

For Event Sourcing, we expect **immutable** events are written to an event log (append-only) to reflect things happened at application level, rather than on lower level.
This helps us better understand why things happen, like 

For example, storing the event “student cancelled their course enrollment” clearly expresses the intent of a single action in a neutral fashion, whereas the side effects “one entry was deleted from the enrollments table, and one cancellation reason was added to the student feedback table” embed a lot of assumptions about the way the data is later going to be used.

New side effect to easily be **chained** off the existing event (like a place can be offered to next person).

---

\*It shoud be noted that user usually prefer seeing current states of system, rather than history of modifications.
**Change Data Capture** can discard former events and only keep the latest value, but **Event Sourcing** usually needs the entire history as later event do not override prior events.
This is a **limition of immutability**, and can be optimized using **snapshot**.

The philosophy of event sourcing is to distinguish **events** and **commands**.
User's request is initially a command, and may fail due to violation of integrity condition. However, if it is accepted, it becomes a **durable** and **immutable** event. It cannot be rejected by consumer of the event stream.
Any validation must happen before a command is executed.

It should be noted that **mutable** state (come with **accoutability**, and is good for analyzing) and append-only log of **immutable** events do not contradict each other.
Database is a cache of a subset of the log, containing the latest values.
\* append only log is more friendly for achieving **atomicity** and removing **non-determinism**.


**Command Query Responsibility Segregation** (CQRS): Derive serval (**read-oriented**) views from the same event log. We can have separate read-optimized view for the new feature, without changing the existing system.
This breaks the **design fallacy** that data must be written in the same form as it will be queried. This can also help resolving the debate around normalization and **denormalization** (such view can be translated from event log).

Limitation of **event sourcing** and **change data capture** is that the event log are usually **asynchronous**, so the read view may not be synced. We can either synchronously update the read view or use a **total order broadcast**.

---

- For small dataset with high rate of updates and deletes, Immutability may result in large history and performance of **compaction** and **garbage collection** becomes crucial for operational robustness 
- For **privacy / compliance** concern, we may want to remove erroneous ifnormation or contain accidental leakage. We may need to **rewrite** history and pretend that data was **never written** (called **excision** or **shunning**).
\* Note that truly delete data can be challenging, because copies can live in many places rather than overwritten in place, we just try to make retrival of data harder.

---

### Processing Streams

A piece of code that processes streams to produce derived streams is known as an **operator** or a **job**.
The input is consumed in **read-only** fashion and writes to a different location in **append-only** fashion.

Since stream is endless, we can **NOT** use mapping operations such as transforming and filtering (sort-merge) records. Also, it is impossible to restart from beginning after a crash.

Stream is widely used for **monitoring** purpose requesting pattern matching and correlations.
Other applications include: 
- **Complex event processing** (search for certain patterns of events in a stream, such pattern may described using high-level declarative query language or GUI, then maintain a state machine. If detected, a complex event is emitted) In such cases, queries become *long-term*.
- **Stream analytics**: towards **aggregations** and **statistical** metrics, usually over fixed time intervals (e.g., averaged request counts and latency in different percentiles). The time interval over which you aggregate is known as a **window**, and probabilistic algorithms are sometimes used like **Bloom filters** and **HyperLogLog**
- **Maintaining materialized views**: deriving an alternative view onto some dataset for query purpose, and update it whenever data changes. However, we may need to maintain all evenets forever, which is against the assumption of a time window.
- **Search on streams**: we may also need to search individual events based on complex criteria (**Elasticsearch**'s **percolator** can support this). We can store (potentially index) queries and ducuments to dynamically search individual events.


**Clock** can be a big challenge in stream processing, as we do not have a unified reliable clock to rely on, and we need timestamp to detemine window.

One mitigation solution is to log three timestamps:
the time an event occured (**device clock**), the **device clock** when it was sent to the server and the **server clock** when it is received.
By subtracting the second timestamp from the third, you can estimate the **offset** between the device clock and the server clock 

---

Some different types of windows which got commonly used:
- **Tumbling window**: fixed-lengthed, every event belongs to exactly one window. Can be implemented by taking each event timestamp and **rounding** it down to the nearest minute.
- **Hopping window**: fixed-lengthed, allow windows to **overlap** to provide smoothing.
- **Sliding window**: Contains all the events that occur within some interval of each other. Can be implemented by a **buffer** of events, and remove old events when they expire from the window.
- **Session window**: No fixed duration, just group all events for the same user occur closely together in time. Ends when user become **inactive**. 

---

### Stream Joins 
- **Stream-stream join** (window join): We may need to link search and click activity (within certain time window) to let them sharing the same session ID (note that you need to learn accurate click-through rate, to learn searches which did not bring clicks events). We can use a stream processor to merge such activities by ID.
- **Stream-table join** (stream enrichment): Enrich the activity events with information from the table. If the database querying is slow, consider loading the database copy (may need to be updated by **change data capture**) to the stream processor.
- **Table-table join** (materialized view maintenance): Cache maintenance similar to the example provided at the beginning of this book. When celebrity tweets, sync it too all followers' tiemlines. We can maintain a **materialized view** for a query that joins two tables

For the aboce cases, **time dependency** is important, as data in certain DB can change (e.g., tax rate), which prevents us from getting the same result rerunning the same job.
In data warehouse, it is called **Slowly Changing Dimension** (SCD). We can use a **unique** identifier for a particular version of the joined record (e.g., whenever tax rate changes). This makes the join deterministic, but will also make log compaction impossible.

---

# Fault Tolerance
**Exactly-once Semantics / Effectively-Once**: though some tasks / records may failed and processed multiple times, the visible effect is as if they have only been processed once.

However, stream is **infinite**, so we cannot make output until finished.

**Microbatching**: break the stream into small blocks, and treat each block like a miniature batch process (in a implicit tumbling window).
Can generate **rolling checkpoints** of state and write them to durable storage (however, if message is sent to external message broker like email, checkpoint is not sufficient to make it effective once, and will need **2PC**)

**Idempotence**: We can require certain operation which can be performed multiple times, but effect only once.







