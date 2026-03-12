---
title: Interview Prep Hub
date: 2026-03-12 01:00:00
type: interview
comments: false
---

A structured study guide for technical interviews, organized by topic area. Each section links to detailed blog posts with concepts, examples, and takeaways you can review before interviews.

---

## System Design (DDIA)

Core distributed systems concepts from *Designing Data-Intensive Applications* by Martin Kleppmann, organized by interview theme.

### Data Storage and Retrieval

| Concept | Key Points | Notes |
|---------|-----------|-------|
| LSM-Trees vs B-Trees | LSM: write-optimized, append-only segments. B-Tree: read-optimized, in-place updates. | [Note 5](/2019/05/18/Designing-Data-Intensive-Applications-Note-5/), [Note 6](/2019/05/18/Designing-Data-Intensive-Applications-Note-6/) |
| Data Models | Relational (tables + joins), Document (nested, schema-on-read), Graph (relationships) | [Note 4](/2019/05/18/Designing-Data-Intensive-Applications-Note-4/) |
| OLTP vs OLAP | OLTP: row-oriented, low-latency queries. OLAP: column-oriented, analytical aggregations. | [Note 7](/2019/05/18/Designing-Data-Intensive-Applications-Note-7/) |
| Encoding and Schema Evolution | Protobuf, Avro, Thrift for forward/backward compatibility. Schema registries. | [Note 8](/2019/05/18/Designing-Data-Intensive-Applications-Note-8/), [Note 9](/2019/05/18/Designing-Data-Intensive-Applications-Note-9/) |

### Replication and Consistency

| Concept | Key Points | Notes |
|---------|-----------|-------|
| Leader-Based Replication | Single leader handles writes, followers replicate. Tradeoff: simplicity vs write bottleneck. | [Note 10](/2019/05/18/Designing-Data-Intensive-Applications-Note-10/), [Note 11](/2019/05/18/Designing-Data-Intensive-Applications-Note-11/) |
| Replication Lag | Read-after-write, monotonic reads, consistent prefix reads. Eventual consistency pitfalls. | [Note 12](/2019/05/18/Designing-Data-Intensive-Applications-Note-12/) |
| Multi-Leader and Leaderless | Multi-leader: multi-datacenter writes. Leaderless: quorum reads/writes (R + W > N). | [Note 13](/2019/05/18/Designing-Data-Intensive-Applications-Note-13/) |
| Consistency and Linearizability | Linearizability = behaves as if single copy. Needed for locks, leader election, uniqueness. | [Note 17](/2019/05/18/Designing-Data-Intensive-Applications-Note-17/) |

### Partitioning and Scaling

| Concept | Key Points | Notes |
|---------|-----------|-------|
| Partitioning Strategies | Key-range (sorted, range scans) vs hash (uniform distribution). Compound keys for locality. | [Note 14](/2019/05/18/Designing-Data-Intensive-Applications-Note-14/) |
| Hot Spots | Skewed partitions from popular keys. Mitigate with salting, compound keys, or application-level sharding. | [Note 14](/2019/05/18/Designing-Data-Intensive-Applications-Note-14/) |
| Scalability Patterns | Vertical vs horizontal scaling. Shared-nothing architectures. Load descriptions via percentiles. | [Note 1](/2019/05/18/Designing-Data-Intensive-Applications-Note-1/), [Note 2](/2019/05/18/Designing-Data-Intensive-Applications-Note-2/) |

### Transactions and Fault Tolerance

| Concept | Key Points | Notes |
|---------|-----------|-------|
| ACID vs BASE | ACID: strong guarantees, single-node. BASE: relaxed consistency, higher availability. | [Note 15](/2019/05/18/Designing-Data-Intensive-Applications-Note-15/) |
| Isolation Levels | Read Committed, Snapshot Isolation (MVCC), Serializable. Each prevents different anomalies. | [Note 15](/2019/05/18/Designing-Data-Intensive-Applications-Note-15/) |
| Two-Phase Commit (2PC) | Coordinator-based distributed commit. Blocking if coordinator fails. | [Note 15](/2019/05/18/Designing-Data-Intensive-Applications-Note-15/) |
| Distributed System Faults | Network partitions, clock skew, process pauses. Design for partial failures. | [Note 16](/2019/05/18/Designing-Data-Intensive-Applications-Note-16/) |

### Data Pipelines

| Concept | Key Points | Notes |
|---------|-----------|-------|
| Batch Processing | MapReduce: map (extract) then reduce (aggregate). Fault tolerance via re-execution. | [Note 18](/2019/05/18/Designing-Data-Intensive-Applications-Note-18/) |
| Stream Processing | Event-driven, low-latency. Window types: tumbling, hopping, sliding, session. | [Note 19](/2019/05/18/Designing-Data-Intensive-Applications-Note-19/) |
| Change Data Capture | Capture DB changes as event stream. Enables derived views, search indexes, caches. | [Note 19](/2019/05/18/Designing-Data-Intensive-Applications-Note-19/) |

> Full series: [DDIA Reading Notes (19 parts)](/series/ddia/)

---

## System Design (Alex Xu)

Practical system design interview patterns from *System Design Interview* by Alex Xu.

| Topic | Key Patterns | Notes |
|-------|-------------|-------|
| Scaling to Millions | CDN, load balancers, database replication, cache layers, message queues | [Chapters 1-9](/2023/10/07/System-Design-Interview-Alex-Xu-Notes-1/) |
| Rate Limiting | Token bucket, sliding window, fixed window algorithms | [Chapters 1-9](/2023/10/07/System-Design-Interview-Alex-Xu-Notes-1/) |
| Notification Systems | Fan-out, third-party service integration, retry strategies | [Chapters 10-16](/2024/01/08/System-Design-Interview-Alex-Xu-Notes-2/) |
| Distributed Architecture | Avoiding single points of failure, database sharding, consistent hashing | [Chapters 10-16](/2024/01/08/System-Design-Interview-Alex-Xu-Notes-2/) |

### System Design Interview Checklist

1. **Clarify requirements**: Functional vs non-functional. Ask about scale, latency, consistency needs.
2. **High-level design**: Draw major components (clients, servers, databases, caches, queues).
3. **Deep dive**: Pick 1-2 components. Discuss data model, API design, scaling strategy.
4. **Trade-offs**: CAP theorem, consistency vs availability, cost vs performance.
5. **Bottlenecks**: Identify hotspots, single points of failure, and how to mitigate.

---

## SQL

Key SQL concepts frequently tested in interviews, drawn from the [SQL Study Notes series (16 parts)](/series/sql/).

### Quick Reference

| Topic | What to Know | Notes |
|-------|-------------|-------|
| JOINs | INNER, LEFT, RIGHT, FULL OUTER, SELF, CROSS. Know when to use each. | [Note 1](/2019/06/29/SQL-Study-Note-1/) |
| Aggregation | GROUP BY + HAVING for filtered aggregates. COUNT, SUM, AVG, MIN, MAX. | [Note 3](/2019/06/29/SQL-Study-Note-3/) |
| Window Functions | ROW_NUMBER, RANK, DENSE_RANK, NTILE. PARTITION BY + ORDER BY. Running totals, moving averages. | [Note 13](/2019/06/30/SQL-Study-Note-13/) |
| CTEs | WITH clause for readable subqueries. Recursive CTEs for hierarchies. | [Note 12](/2019/06/30/SQL-Study-Note-12/) |
| Subqueries | Correlated vs uncorrelated. EXISTS vs IN performance differences. | [Note 1](/2019/06/29/SQL-Study-Note-1/) |
| Indexes | B-Tree default, composite index column order matters, covering indexes avoid table lookups. | [Note 10](/2019/06/30/SQL-Study-Note-10/) |
| Normalization | 1NF (atomic), 2NF (no partial deps), 3NF (no transitive deps). When to denormalize. | [Note 9](/2019/06/30/SQL-Study-Note-9/) |
| Transactions | BEGIN/COMMIT/ROLLBACK. Isolation levels. Deadlock detection. | [Note 7](/2019/06/29/SQL-Study-Note-7/) |
| Query Optimization | EXPLAIN plans, index selection, avoiding SELECT *, reducing subqueries. | [Note 14](/2019/06/30/SQL-Study-Note-14/), [Note 15](/2019/06/30/SQL-Study-Note-15/), [Note 16](/2019/06/30/SQL-Study-Note-16/) |

### Common Interview Patterns

- **Top-N per group**: Use `ROW_NUMBER() OVER (PARTITION BY group_col ORDER BY rank_col) AS rn` then filter `WHERE rn <= N`.
- **Running totals**: `SUM(amount) OVER (ORDER BY date ROWS UNBOUNDED PRECEDING)`.
- **Duplicate detection**: `GROUP BY columns HAVING COUNT(*) > 1`.
- **Self-join for comparisons**: Join a table to itself to compare rows (e.g., employees earning more than their manager).
- **Gap detection**: Use `LAG()` or `LEAD()` window functions to find missing sequences.

---

## Data Science and ML

Core ML concepts for data science interviews from the [DS Study Notes series (9 parts)](/series/ds/).

### Algorithms to Know

| Algorithm | Type | Key Interview Points | Notes |
|-----------|------|---------------------|-------|
| Linear/Logistic Regression | Supervised | Assumptions, regularization, coefficient interpretation | [Note 7](/2020/04/04/DS-Study-Note-7/) |
| Decision Trees | Supervised | Gini vs entropy, pruning, overfitting risk | [Note 8](/2020/05/02/DS-Study-Note-8/) |
| Random Forest | Ensemble | Bagging, feature importance, out-of-bag error | [Note 8](/2020/05/02/DS-Study-Note-8/) |
| Gradient Boosting | Ensemble | Sequential learning, learning rate, shrinkage | [Note 9](/2020/05/20/DS-Study-Note-9/) |
| SVM | Supervised | Maximum margin, kernel trick, soft margin (C parameter) | [Note 5](/2020/02/21/DS-Study-Note-5/) |
| Naive Bayes | Supervised | Independence assumption, Laplace smoothing, text classification | [Note 6](/2020/03/04/DS-Study-Note-6/) |

### Foundational Concepts

| Concept | Key Points | Notes |
|---------|-----------|-------|
| Bias-Variance Tradeoff | High bias = underfitting. High variance = overfitting. Sweet spot minimizes total error. | [Note 2](/2019/10/11/DS-Study-Note-2/) |
| Overfitting | Causes: too many features, insufficient data, high model complexity. Fixes: regularization, cross-validation, early stopping. | [Note 1](/2019/08/17/DS-Study-Note-1/) |
| Regularization | L1 (Lasso): sparse features, feature selection. L2 (Ridge): shrinks all weights, handles multicollinearity. | [Note 7](/2020/04/04/DS-Study-Note-7/) |
| Evaluation Metrics | Precision (false positive cost), Recall (false negative cost), F1 (balanced), AUC-ROC (threshold-independent). | [Note 4](/2020/01/28/DS-Study-Note-4/) |
| Cross-Validation | K-fold: rotate held-out set. Stratified: preserve class balance. Prevents data leakage. | [Note 1](/2019/08/17/DS-Study-Note-1/) |
| Curse of Dimensionality | Distance metrics break down in high dimensions. Feature selection and PCA help. | [Note 3](/2019/10/16/DS-Study-Note-3/) |

### Common ML Interview Questions

- **"When would you use Random Forest vs Gradient Boosting?"** RF: parallel, less tuning, robust to noise. GBM: sequential, higher accuracy, needs careful tuning.
- **"How do you handle imbalanced classes?"** Resampling (SMOTE, undersampling), class weights, adjusted thresholds, use precision-recall over accuracy.
- **"Explain the bias-variance tradeoff."** Model too simple = high bias (misses patterns). Model too complex = high variance (fits noise). Regularization and cross-validation help find the balance.
- **"L1 vs L2 regularization?"** L1 drives coefficients to zero (feature selection). L2 shrinks all coefficients (stability). Elastic Net combines both.

---

## Behavioral Interviews

Frameworks and strategies for behavioral questions, using the STAR method.

> Detailed guide: [Behavioral Interview Questions Crack](/2024/09/17/Behavioral-Interview-Questions-Crack/)

### STAR Method

| Step | What to Include |
|------|----------------|
| **S**ituation | Set the scene. Team size, project type, timeline, stakes. |
| **T**ask | Your specific responsibility. What was expected of you. |
| **A**ction | What YOU did (not the team). Be specific about decisions and reasoning. |
| **R**esult | Quantify impact. Metrics, outcomes, lessons learned. |

### Common Themes to Prepare

- **Leadership/influence**: Times you drove a technical decision or mentored others.
- **Conflict resolution**: Disagreements with teammates or stakeholders, and how you resolved them.
- **Failure and learning**: Projects that went wrong and what you changed afterward.
- **Ambiguity**: Situations with unclear requirements where you had to define the path forward.
- **Cross-team collaboration**: Working across team boundaries, especially with non-technical stakeholders.

---

## Object-Oriented Design (OOD)

> Detailed guide: [Object Oriented Design -- Principles and Practices](/2023/07/09/Object-Oriented-Design/)

### SOLID Principles

| Principle | One-Liner | Interview Tip |
|-----------|-----------|---------------|
| **S**ingle Responsibility | A class should have one reason to change. | Name the class after its single job. |
| **O**pen/Closed | Open for extension, closed for modification. | Use interfaces and strategy pattern. |
| **L**iskov Substitution | Subtypes must be substitutable for base types. | If it breaks when substituted, it is not a valid subtype. |
| **I**nterface Segregation | No client should depend on methods it does not use. | Split fat interfaces into focused ones. |
| **D**ependency Inversion | Depend on abstractions, not concretions. | Constructor injection, interface-based design. |

### OOD Interview Approach

1. **Clarify scope**: What entities, what operations, what constraints?
2. **Identify core objects**: Nouns in the problem become classes.
3. **Define relationships**: Has-a, is-a, uses-a between objects.
4. **Assign behaviors**: Verbs become methods on the appropriate class.
5. **Apply patterns**: Observer, Strategy, Factory, Singleton where they fit.
6. **Discuss trade-offs**: Flexibility vs complexity, inheritance vs composition.

---

## Brainteasers and Puzzles

> Detailed guide: [Collection and Solution of Brainteasers](/2020/01/08/brainteaser-1/)

### Problem Categories

| Category | Example Topics |
|----------|---------------|
| **Probability** | Dice games, card draws, conditional probability, Bayes' theorem |
| **Logic** | Truth-teller/liar puzzles, process of elimination, invariants |
| **Estimation** | Fermi problems (how many piano tuners in Chicago?) |
| **Game Theory** | Backward induction, optimal strategies, Nash equilibrium |
| **Math** | Modular arithmetic, combinatorics, expected value calculations |

### General Approach

1. **Restate the problem** to confirm understanding.
2. **Identify the type** (probability, logic, estimation, game theory).
3. **Start with small cases** -- solve for N=2, N=3, then generalize.
4. **State assumptions** explicitly before calculating.
5. **Think out loud** -- interviewers evaluate your reasoning process, not just the answer.

---

## Study Plan

### 1-Week Sprint

| Day | Focus | Resources |
|-----|-------|-----------|
| Mon | System Design fundamentals | DDIA Notes 1-4, Alex Xu Ch 1-9 |
| Tue | Distributed systems deep dive | DDIA Notes 10-15 (replication, partitioning, transactions) |
| Wed | SQL practice | SQL Notes 1, 3, 10, 12, 13 (joins, aggregation, indexes, CTEs, window functions) |
| Thu | ML algorithms and concepts | DS Notes 1-4 (fundamentals), Notes 5-9 (algorithms) |
| Fri | Behavioral + OOD | Behavioral Questions Crack, OOD Principles |
| Sat | System Design practice | DDIA Notes 16-19 (faults, consistency, batch, stream) + Alex Xu Ch 10-16 |
| Sun | Review weak areas | Re-read concept index at [/concepts/](/concepts/) |

### Key Pages

- [Concept Index](/concepts/) -- searchable index of all 87+ concepts across posts
- [DDIA Series](/series/ddia/) -- 19-part distributed systems deep dive
- [SQL Series](/series/sql/) -- 16-part SQL reference
- [DS Series](/series/ds/) -- 9-part data science and ML review
