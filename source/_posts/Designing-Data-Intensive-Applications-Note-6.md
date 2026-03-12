---
title: Designing Data-Intensive-Applications-Note-6
date: 2024-02-24 09:34:35
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on Indexes and Multi-Column Index solution (R-Tree)."
key_concepts:
  - Database Indexes
  - B-Tree
  - LSM-Tree
takeaways:
  - Use clustered indexes when frequently querying by primary key to avoid extra heap file lookups
  - Apply multi-column concatenated indexes for queries filtering on multiple fields in order
  - Use R-trees for geospatial queries where standard B-tree indexes cannot handle multi-dimensional data
  - Consider in-memory databases like Redis when dataset fits in RAM for significant performance gains
series: DDIA
series_index: 6
---
Discussion on Indexes and Multi-Column Index solution (R-Tree).
{% asset_img cover.png DDIA Chapter 6 cover: Indexes and Multi-Column Index with R-Trees %}
<!-- more -->


### Secondary Index
- The mapping may not be unique, i.e., we may have multiple rows mapped to the same key in secondary index. This can be solved by either 
[1] making each value in that key to be **list** of matching row identifiers, or by 
[2] making each key **unique** (adding a row identifer to the key).
- May help with **Join**.

### Storing values within the index
In index, the key can just be the search keyword, but the value can be: 
[1] **Actual row** (or document / vertex) in question
[2] **Reference** to the row stored elsewhere 
(That file is called **heap** file, in no particular order).

Heap file helps: 
1. Eliminating **duplication**, because if there lies multiple secondary index, only the reference of data is stored; 
2. Efficient at **overwriting** values, if new value is no larger than the old value. 

Otherwise, the new value needs to be moved to somewhere with enough space. In that case, we can either update all secondary indexes to be updated to point to the new location, or leave a **forwarding pointer** in place.

- **Clustered index**: If extra hop from index to heap file is too much of performance penalty for reads, we can directly store **indexed row** within index.
E.g., In MySQL’s **InnoDB** engine, the **primary key** of a table is always a clustered index and secondary indexes refer to the primary key. In SQL server, you can specify **one** clustered index per table.
- **Compromise between clustered / non-clustered index**: covering index or index with included columns, only stores some of the columns within the index.     Both cluster and covering index can speed up the reads but require more storage / write overhead.

---

### Multi-column indexes:
- Can help querying **multiple** columns of a table
- Trivial implementation can be **concatenated index**, which concat multiple columns. This is not very flexible as it is hard coded, you can hardly search by some column’s **sub-pattern**.
- Standard B-Tree / LSM-tree index can hardly answer quries which **restrict range** on multiple columns.
- **Implementation** 1: To translate a multi-dimensional location into a single number using a **space-filling curve**, and then to use a regular B-tree index
- **Implementation** 2: A better choice is using spatial indexes like **R-trees**.


### R-Tree (R for Rectangle):
- An generalization of B-tree to **high-dim** space. Used **Minimal Bounding Rectangle** (MBR) for space dividing. That is to say, just like segment tree, we want a spatial “rectangle tree” so that given a node, we can get the sub-nodes / leaves belonging to that region. This tree can be **multi-way**.

{% asset_img 1.png R-Tree structure showing Minimal Bounding Rectangles for spatial indexing %}

- **Structure of leaf nodes**: leaf nodes are saved as tuples of `(l, tuple-identifier)`. Where `tuple-identifer` is a n-dim vector (can be realized as a single record / data point) and `l` is a n-dim rectangle which can exactly include all the datapoints belonging to this leaf node.
- **Stucture of non-leaf nodes**: `(l, child-pointer)`, where `l` is the n-dim rectangle, and `child-point points` to the child node(s).

**Variants of R-tree**: 
1. **R\* tree** (use **re-insertion** to reduce overlap and improve query performance, using a combination of a revised **node split** algorithm and the concept of forced reinsertion at node overflow). 
R-tree is sensitive to the order of insertion, thus we can improve it by: when a node overflows, a portion of its entries are removed and reinserted, limited to **one** time to avoid indefinite **cascade re-insertion**.)
2. **R+ Tree**: a tradeoff betweem **R-tree** and **kd-tree**. If needed, insert an object into multiple leaves to avoid overlapping of internal nodes. Minimal coverage reduces the amount of "dead space" (empty area), and reduces the set of search path to the leaves.
The difference is that R+ Tree is not guaranteed to be at least **half-filled**, the entries of any internal node do not overlap, and an object ID maybe stored in more than one leaf node.

---

### Full-text search and fuzzy indexes:
- **Motivation**: Instead of search the exact value, we want to allow search for **similar** keys like mis-spelled words.
- **Full text search**: Include **synonyms** of the word, to ignore **grammatical variations** of
words, and to search for occurrences of words **near** each other in the same document, and support various other features that depend on linguistic analysis of the text.
- **Lucene** allows searching of words within a certain **edit distance**, using quasi-SSTable structure to get the **offset** in the sorted file where they need to look for the candidate keys.   
- In **LevelDB**, this in-memory index is a sparse collection of some of the keys, but in **Lucene**, the in-memory index is a **finite state automaton** over the characters in the keys, similar to a **trie**.

### Keep everything in memory (persistent memory storage?):
- Disks are **cheaper** and **durable** (will **NOT** lose data when power off), but needs to be laid out carefully for good performance on reads and writes.
- Now memory is cheaper, and for use cases like **Memcached**, data loss is acceptable. For durability required by database, we can **log** changes to disk, **replicating** in-memory state to other machines, this also helps with back-up / inspection and analysis.
- Memory databases are faster because they can avoid the overheads of **encoding** in-mem data to disk form. They can also provide **priority queques** and **sets** (by **Redis**, e.g.) which are hard to implement on disk.
- We can actually support memory database which requires more space than the memory (overlay?) When there is no space, **evict** content to disk, when needed, **load** it back. It is like OS memory management (swap) but in **record granularity**. 














