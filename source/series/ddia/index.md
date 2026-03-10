---
title: "Designing Data-Intensive Applications: Reading Notes"
date: 2026-03-09 01:00:00
type: series
comments: false
---

A 19-part series of reading notes on Martin Kleppmann's *Designing Data-Intensive Applications* (DDIA). The book covers the fundamental ideas behind reliable, scalable, and maintainable data systems -- from single-node storage engines to distributed architectures and stream processing pipelines.

These notes follow the book's three-part structure: foundations of data systems, distributed data, and derived data. Each note captures the key concepts, trade-offs, and design patterns from one or two chapters.

---

## Topic Overview

```mermaid
mindmap
  root((DDIA))
    Part I: Foundations
      Reliability, Scalability, Maintainability
      Data Models and Query Languages
      Storage and Retrieval
      Encoding and Evolution
    Part II: Distributed Data
      Replication
      Partitioning
      Transactions
      Distributed System Challenges
      Consistency and Consensus
    Part III: Derived Data
      Batch Processing
      Stream Processing
```

---

## Reading Notes

### Part I: Foundations of Data Systems

1. {% post_link Designing-Data-Intensive-Applications-Note-1 "Note 1: Reliability and Key Concepts" %}
2. {% post_link Designing-Data-Intensive-Applications-Note-2 "Note 2: Scalability and Performance" %}
3. {% post_link Designing-Data-Intensive-Applications-Note-3 "Note 3: Maintainability" %}
4. {% post_link Designing-Data-Intensive-Applications-Note-4 "Note 4: Data Models and Query Languages" %}
5. {% post_link Designing-Data-Intensive-Applications-Note-5 "Note 5: Storage and Retrieval (Log-Structured)" %}
6. {% post_link Designing-Data-Intensive-Applications-Note-6 "Note 6: Storage and Retrieval (Indexes)" %}
7. {% post_link Designing-Data-Intensive-Applications-Note-7 "Note 7: OLTP vs OLAP and Data Warehousing" %}
8. {% post_link Designing-Data-Intensive-Applications-Note-8 "Note 8: Encoding and Evolution" %}
9. {% post_link Designing-Data-Intensive-Applications-Note-9 "Note 9: Data Flow (Databases, REST, RPC)" %}

### Part II: Distributed Data

10. {% post_link Designing-Data-Intensive-Applications-Note-10 "Note 10: Replication and Scaling" %}
11. {% post_link Designing-Data-Intensive-Applications-Note-11 "Note 11: Replication Strategies" %}
12. {% post_link Designing-Data-Intensive-Applications-Note-12 "Note 12: Replication Lag and Consistency" %}
13. {% post_link Designing-Data-Intensive-Applications-Note-13 "Note 13: Multi-Leader and Leaderless Replication" %}
14. {% post_link Designing-Data-Intensive-Applications-Note-14 "Note 14: Partitioning" %}
15. {% post_link Designing-Data-Intensive-Applications-Note-15 "Note 15: Transactions and ACID" %}
16. {% post_link Designing-Data-Intensive-Applications-Note-16 "Note 16: Distributed System Faults" %}
17. {% post_link Designing-Data-Intensive-Applications-Note-17 "Note 17: Consistency and Linearizability" %}

### Part III: Derived Data

18. {% post_link Designing-Data-Intensive-Applications-Note-18 "Note 18: Batch Processing" %}
19. {% post_link Designing-Data-Intensive-Applications-Note-19 "Note 19: Stream Processing" %}
