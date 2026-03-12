---
title: "DDIA Cheat Sheet"
date: 2026-03-12
type: "page"
comments: false
---

# Designing Data-Intensive Applications -- Quick Reference

A condensed reference of all 19 DDIA study notes. Use this for interview prep and concept review.

---

## 1. Foundations (Notes 1-3)

### Three Pillars of Data Systems

| Pillar | Goal | Key Techniques |
|--------|------|----------------|
| Reliability | System works correctly despite faults | Redundancy (HW/SW), process isolation, crash-restart, monitoring |
| Scalability | Handle growing load gracefully | Horizontal scaling, caching, fan-out strategies |
| Maintainability | Easy to operate, understand, evolve | Good abstractions, monitoring, automation, simple design |

**Fault vs Failure**: A fault is a component deviation; a failure is system-wide service loss.

### Measuring Performance

| Metric | What It Tells You |
|--------|-------------------|
| p50 (median) | Typical user experience |
| p95 | Worst case for 1 in 20 requests |
| p99 | Tail latency; important for SLAs |

- Use **percentiles**, not averages, for response time
- **Head-of-line blocking**: one slow request delays all queued behind it
- **Fan-out-on-write** (precompute) vs **fan-out-on-read** (compute at read time)

---

## 2. Data Models & Query Languages (Note 4)

| Model | Best For | Weakness |
|-------|----------|----------|
| Relational | Many-to-many relationships, joins | Schema rigidity, impedance mismatch |
| Document (JSON) | Self-contained records, nested data | Poor joins, deep nesting limits |
| Graph | Relationships as important as entities | Complexity, fewer mature tools |

**Query Paradigms**: Declarative (SQL) > Imperative (IMS) for optimization. MapReduce sits between (pure functions, no side effects).

---

## 3. Storage Engines (Notes 5-6)

### LSM-Tree vs B-Tree

| | LSM-Tree | B-Tree |
|---|---------|--------|
| Optimized for | Writes (sequential I/O) | Reads (in-place updates) |
| Structure | Memtable + SSTables on disk | Fixed-size pages (4KB), branching factor ~500 |
| Compaction | Background merge of sorted runs | Page splits on overflow |
| Write amplification | From compaction | From WAL + page writes |
| Crash recovery | WAL + memtable rebuild | WAL replay |

### Index Types

| Type | Use Case |
|------|----------|
| Hash index | Exact key lookup (in-memory) |
| B-tree / B+ tree | Range queries, general purpose |
| LSM + Bloom filter | Write-heavy with occasional reads |
| R-tree | Geospatial / multi-dimensional |
| Full-text (Lucene) | Synonym, proximity, fuzzy search |
| Clustered index | Frequent primary key lookups (stores row in index) |
| Covering index | Query answered entirely from index |

### In-Memory Databases
- Faster not because they avoid disk reads (OS caches anyway) but because they skip encoding overhead
- Enable data structures hard on disk: priority queues, sets (Redis)

---

## 4. OLTP vs OLAP (Note 7)

| | OLTP | OLAP |
|---|------|------|
| Query pattern | Small reads/writes by key | Aggregate scans over many rows |
| Users | End users via application | Internal analysts |
| Data size | GB-TB | TB-PB |
| Storage | Row-oriented | Column-oriented (Parquet) |

**Star Schema**: Central fact table (events) + dimension tables (who/what/where/when/why).

**Column Storage Optimizations**: Bitmap encoding, run-length encoding, sort order as index, vectorized processing (SIMD), materialized aggregates / OLAP cubes.

---

## 5. Encoding & Schema Evolution (Note 8)

| Format | Schema | Size | Evolution |
|--------|--------|------|-----------|
| JSON/XML | Optional | Verbose | Flexible but no guarantees |
| Protocol Buffers | Required (field tags) | Compact (varint) | Add optional fields; never reuse deleted tags |
| Avro | Writer + Reader schemas | Most compact | Match by field name; add/remove fields with defaults |
| Thrift | Required (field tags) | Compact | Similar to Protobuf |

**Compatibility Rules**:
- **Backward**: New code reads old data (add optional fields with defaults)
- **Forward**: Old code reads new data (ignore unknown fields)

---

## 6. Data Flow Patterns (Note 9)

| Pattern | Pros | Cons |
|---------|------|------|
| REST | Simple, good tooling, cacheable | Synchronous, coupled |
| RPC | Looks like local call | Network is NOT local (timeouts, retries, type mismatches) |
| Message Broker | Decoupled, buffered, redelivery | Added infrastructure complexity |
| Actor Model | No shared state, location transparent | Learning curve, migration complexity |

**RPC pitfalls**: Network unpredictable, requests may execute multiple times, large objects serialize poorly. Design idempotent operations.

---

## 7. Replication (Notes 10-13)

### Replication Strategies

| Strategy | Writes | Consistency | Use Case |
|----------|--------|-------------|----------|
| Single-leader | Leader only | Strong (if sync) | Default for most systems |
| Multi-leader | Multiple leaders | Eventual | Multi-datacenter, offline clients |
| Leaderless (Dynamo) | Any node | Configurable (quorum) | High availability, partition tolerance |

### Replication Lag Problems & Solutions

| Problem | Symptom | Solution |
|---------|---------|----------|
| Read-after-write | User doesn't see own update | Read from leader for recently-modified data |
| Monotonic reads | Data appears to go backward | Route same user to same replica |
| Consistent prefix | Effect before cause | Keep causally-related writes on same partition |

### Replication Log Types

| Type | Mechanism | Trade-off |
|------|-----------|-----------|
| Statement-based | Forward SQL statements | Breaks with RAND(), NOW(), triggers |
| WAL shipping | Send storage engine log | Couples to storage format; blocks version upgrades |
| Logical (row-based) | Row-level change log | Decoupled; enables zero-downtime upgrades |
| Trigger-based | Application-level hooks | Flexible but slow and error-prone |

### Quorum Formula
**w + r > n** guarantees overlap for reading latest write. Sloppy quorum + hinted handoff trades consistency for availability.

### Conflict Resolution (Multi-leader / Leaderless)

| Approach | How It Works | Data Loss? |
|----------|-------------|------------|
| Last-Write-Wins (LWW) | Highest timestamp wins | Yes (concurrent writes lost) |
| Version Vectors | Track causality per replica | No (keeps siblings) |
| CRDTs | Auto-merge data structures | No |
| Operational Transform | 3-way merge (Google Docs) | No |

### Chain Replication (CRAQ)
HEAD receives writes, propagates down chain, TAIL confirms. Any node serves reads (version vector + tail check). Tolerates n-1 failures.

---

## 8. Partitioning / Sharding (Note 14)

| Strategy | Pros | Cons |
|----------|------|------|
| Key range | Efficient range queries | Hot spots on sequential keys |
| Hash of key | Even distribution | No range queries |
| Compound key | Hash first part, range on rest | Application must design key |

### Secondary Indexes on Partitions

| Type | Write | Read |
|------|-------|------|
| Document-partitioned (local) | Fast (update local index) | Scatter/gather across all partitions |
| Term-partitioned (global) | Slow (distributed transaction) | Single partition read |

### Rebalancing Approaches
- **Fixed partitions**: More partitions than nodes; move whole partitions
- **Dynamic**: Split/merge based on size (HBase)
- **Proportional**: Fixed partitions per node; new node splits random existing

**Request Routing**: (1) Any node forwards, (2) Routing tier, (3) Client-aware. ZooKeeper for coordination.

---

## 9. Transactions (Note 15)

### ACID vs BASE

| ACID | BASE |
|------|------|
| Atomicity, Consistency, Isolation, Durability | Basically Available, Soft state, Eventual consistency |
| Strong guarantees, higher cost | Weaker guarantees, higher availability |

### Isolation Levels

| Level | Dirty Read | Non-repeatable Read | Phantom Read | Performance |
|-------|-----------|---------------------|-------------|-------------|
| Read Uncommitted | Possible | Possible | Possible | Fastest |
| Read Committed | Prevented | Possible | Possible | Good |
| Snapshot Isolation (MVCC) | Prevented | Prevented | Possible | Good |
| Serializable | Prevented | Prevented | Prevented | Slowest |

### Serializability Implementations

| Approach | How | Trade-off |
|----------|-----|-----------|
| Serial execution | Single-threaded, stored procedures | Simple but limited throughput |
| Two-Phase Locking (2PL) | Shared/exclusive locks held until commit | Deadlock risk, high contention |
| SSI (Serializable Snapshot Isolation) | Optimistic; abort on stale read detection | Best performance; abort overhead |

### Preventing Lost Updates
- **Atomic operations**: `UPDATE t SET v = v + 1`
- **Compare-and-set**: `UPDATE t SET v = new WHERE v = old`
- **Explicit locks**: `SELECT ... FOR UPDATE`

**Write Skew**: Two transactions read same data, update different rows, violating a constraint. Only serializable isolation prevents this.

---

## 10. Distributed System Challenges (Note 16)

### Unreliable Components

| Component | Problem | Mitigation |
|-----------|---------|------------|
| Network | Packets lost, delayed, duplicated | Timeouts (but duration uncertain) |
| Clocks | Wall clocks jump (NTP); drift ~17s/day | Use monotonic clocks for duration; logical clocks for ordering |
| Processes | GC pauses, VM suspension, context switches | Fencing tokens for leader leases |

**Phi Accrual Failure Detector**: Adaptive timeout based on heartbeat probability distribution.

**Fencing Tokens**: Lock service issues monotonically-increasing tokens; storage rejects writes with old tokens.

### System Models

| Network | Node Failures |
|---------|--------------|
| Synchronous (bounded delay -- unrealistic) | Crash-stop (permanent) |
| Partially synchronous (usually bounded) | Crash-recovery (resume with disk) |
| Asynchronous (no timing guarantees) | Byzantine (arbitrary behavior) |

**Safety** = nothing bad happens. **Liveness** = something good eventually happens.

---

## 11. Consensus & Linearizability (Note 17)

### Linearizability vs Serializability

| | Linearizability | Serializability |
|---|----------------|-----------------|
| Scope | Single object recency | Multi-object transaction isolation |
| Guarantee | Reads see latest write | Transactions appear serial |
| Combined | Strict Serializability (strong-1SR) | |

### CAP Theorem (Simplified)
During a network partition, choose: **Linearizability** (wait for network) OR **Availability** (serve possibly stale data). Not a general design guide.

### Two-Phase Commit (2PC)
1. **Prepare**: Coordinator asks all participants "can you commit?"
2. **Commit/Abort**: If all say yes, commit; otherwise abort
- **Blocking protocol**: If coordinator fails after prepare, participants stuck in-doubt
- Participants surrender abort right after voting "yes"

### Consensus Algorithms
Raft, Paxos, Viewstamped Replication, Zab -- all implement total order broadcast. Require strict majority (2f+1 nodes tolerate f failures).

### Ordering & Causality
- **Causal consistency**: Strongest model that doesn't require waiting for network
- **Lamport timestamps**: (counter, node_id) pairs for total ordering
- **Total order broadcast**: Reliable + totally ordered delivery = repeated consensus

---

## 12. Batch Processing (Note 18)

### Unix Philosophy Applied to Data
Compose single-purpose tools via pipes. Input/output = immutable files. Enables experimentation and restart at any stage.

### MapReduce Pipeline
1. **Map**: Input record -> key-value pairs
2. **Shuffle**: Hash by key, route to reducers
3. **Reduce**: Process all values for a key -> output

### Join Strategies

| Join Type | When to Use | How |
|-----------|-------------|-----|
| Sort-merge (reduce-side) | General case | Both inputs sorted by join key |
| Broadcast hash (map-side) | One input small | Load small dataset into mapper memory |
| Partitioned hash (map-side) | Pre-partitioned identically | Each mapper joins its own partition |

### MapReduce vs Dataflow Engines (Spark, Flink, Tez)

| | MapReduce | Dataflow |
|---|-----------|----------|
| Intermediate data | Materialized to HDFS | Pipelined (memory/local disk) |
| Operators | Strict map + reduce | Flexible (any function) |
| Fault tolerance | Rerun failed tasks | Lineage tracking (RDD), recompute |
| Performance | Slower (materialization overhead) | Faster (less I/O) |

---

## 13. Stream Processing (Note 19)

### Message Delivery Models

| System | Ordering | Replay | Pattern |
|--------|----------|--------|---------|
| Traditional broker (RabbitMQ) | Per-consumer | No (ACK deletes) | Load balance or fan-out |
| Log-based broker (Kafka) | Per-partition | Yes (offset-based) | Fan-out; load balance per partition |

### Window Types for Aggregation

| Window | Description |
|--------|-------------|
| Tumbling | Fixed-size, non-overlapping |
| Hopping | Fixed-size, overlapping (slide < size) |
| Sliding | All events within interval of each event |
| Session | Same user, gap-based grouping |

### Stream Joins

| Join | What It Does |
|------|-------------|
| Stream-stream | Match events within a time window |
| Stream-table | Enrich events with database lookup (CDC-updated local copy) |
| Table-table | Materialized view maintenance |

### Change Data Capture (CDC)
Capture database changes, replicate to derived systems (indexes, caches, warehouses). Log compaction keeps latest value per key.

### Exactly-Once Semantics
Achieve through **idempotent operations** (preferred) or microbatching/checkpoints. Avoid dual writes (race condition risk).

### Event Sourcing
Immutable append-only log of application events. Derive multiple read views (CQRS). Supports new features via new views without system changes.

---

## Quick Decision Guide

**Storage engine?** Write-heavy -> LSM-tree. Read-heavy -> B-tree.

**Data model?** Joins needed -> Relational. Self-contained docs -> Document. Complex relationships -> Graph.

**Replication?** Single datacenter -> Single-leader. Multi-DC -> Multi-leader. Max availability -> Leaderless.

**Partitioning?** Range queries -> Key range. Even distribution -> Hash. Both -> Compound key.

**Isolation level?** Most workloads -> Snapshot Isolation. Need serializability -> SSI. Max throughput -> Read Committed.

**Processing?** Bounded data -> Batch (Spark). Unbounded / real-time -> Stream (Kafka + Flink). Mixed -> Lambda/Kappa architecture.
